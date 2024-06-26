from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from catalog.models import Product, Version
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse, reverse_lazy
from catalog.forms import ModerProductForm, ProductForm, VersionForm
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from config import settings
from catalog.services import get_category_list


class ProductListView(ListView):
    model = Product
    
    def get_context_data(self, **kwards):
        context_data = super().get_context_data(**kwards)
        context_data['user'] = self.request.user
        context_data['categories'] = get_category_list()
        return context_data
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publicated=True)
        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")

            
    def form_valid(self, form):
        print(self.request.user.id)
        new_product = form.save(commit=False)
        new_product.user = self.request.user
        new_product.publicated = True
        new_product.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        return context
    
            
    


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.change_product'
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object
    
    def get_form_class(self) -> type[BaseModelForm]:
        if self.request.user.is_staff:
            return ModerProductForm
        else:
            return ProductForm
            
    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            versions = Version.objects.filter(product=self.object)
            for item in versions:
                item.current = False
                item.save()
            last = sorted(versions, key=lambda x: x.add_date, reverse=True)
            print(last)
            last[0].current = True
            last[0].save()
        return super().form_valid(form)

    def get_context_data(self, **kwards):
        context_data = super().get_context_data(**kwards)
        ProductFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        context_data['categories'] = get_category_list()
        return context_data

    def get_success_url(self):
        return reverse("catalog:view", args=[self.kwargs.get("pk")])


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        if settings.CACHE_ENABLED:
            key = f'last_{self.object.pk}'
            last = cache.get(key)
            if last is None:
                list = self.object.version_set.all()
                last = sorted(list, key=lambda x: x.add_date, reverse=True)[0]
                cache.set(key, last)
        else:
            list = self.object.version_set.all()
            last = sorted(list, key=lambda x: x.add_date, reverse=True)[0]
        
        context["last"] = last
        return context
    
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        if settings.CACHE_ENABLED:
            key = f'object_{self.kwargs["pk"]}'
            object = cache.get(key)
            if object is None:
                object = Product.objects.get(pk = self.kwargs['pk'])
                cache.set(key, object)
        else:
            object = Product.objects.get(pk = self.kwargs['pk'])
        return object


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:index")
    permission_required = 'catalog.delete_product'
    
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        
        return self.object
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        return context


class ProductContacts(TemplateView):
    model = Product
    http_method_names = ["get"]

    def get(self, request, *args, **kwards):
        return render(request, "catalog/contacts.html")
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        return context


class ProductThanks(TemplateView):
    model = Product
    http_method_names = ["post"]

    def post(self, request, *args, **kwards):
        return render(request, "catalog/thanks.html")


class ProductAuth(TemplateView):
    model = Product
    http_method_names = ["post", "get"]

    def post(self, request, *args, **kwargs):
        return render(request, "catalog/need.html")
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category_list()
        return context
