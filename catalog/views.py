from django.shortcuts import render
from catalog.models import Product
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views import View


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"

class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:index')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')

    def get_success_url(self):
        return reverse('catalog:view', args=[self.kwargs.get('pk')])

class ProductDetailView(DetailView):
    model = Product

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')

# Create your views here.


class ProductContacts(SingleObjectMixin, View):
    model = Product
    
    def get(self, request, *args, **kwards):
        return render(request, 'catalog/contacts.html')

class ProductThanks(SingleObjectMixin, View):
    model = Product

    def post(self, request, *args, **kwards):
        return render(request, 'catalog/thanks.html')

