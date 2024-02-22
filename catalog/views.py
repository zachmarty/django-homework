from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
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
from catalog.forms import ProductForm, VersionForm
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(ListView):
    model = Product
    
    def get_context_data(self, **kwards):
        context_data = super().get_context_data(**kwards)
        context_data['user'] = self.request.user
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")
    login_url = reverse_lazy("users:login")

            
    def form_valid(self, form):
        print(self.request.user.id)
        new_product = form.save(commit=False)
        new_product.user = self.request.user
        new_product.save()
        return super().form_valid(form)
    
    
            
    


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    login_url = reverse_lazy("users:login")
            
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
        return context_data

    def get_success_url(self):
        return reverse("catalog:view", args=[self.kwargs.get("pk")])


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        versions = Version.objects.filter(product=self.object)
        last = sorted(versions, key=lambda x: x.add_date, reverse=True)
        if len(last) > 0:
            context["last"] = last[0]
        return context
    
    login_url = reverse_lazy("users:login")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:index")
    
    login_url = reverse_lazy("users:login")


class ProductContacts(TemplateView):
    model = Product
    http_method_names = ["get"]

    def get(self, request, *args, **kwards):
        return render(request, "catalog/contacts.html")


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
