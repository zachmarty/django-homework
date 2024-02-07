from typing import Any
from django.db.models.query import QuerySet
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
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from catalog.forms import ProductForm, VersionForm
from django.forms import inlineformset_factory


class ProductListView(ListView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")

    def form_valid(self, form):
        new_product = form.save()
        new_product.save()
        version = Version.objects.create(product=new_product)
        version.v_name = "created"
        version.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    
    def form_valid(self, form):
        new_record = form.save()
        new_record.save()
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            previous = Version.objects.filter(product = new_record)
            print(previous)
            for item in previous:
                item.current = False
                item.save()
            last = sorted(previous, key=lambda x: x.v_number)
            self.object.v_number = last[0].v_number + 1
            formset.save()
            self.object.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwards):
        context_data = super().get_context_data(**kwards)
        RecordFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = RecordFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = RecordFormset(instance=self.object)
        return context_data

    def get_success_url(self):
        return reverse("catalog:view", args=[self.kwargs.get("pk")])


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:index")


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
