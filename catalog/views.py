from django.shortcuts import render
from catalog.models import Product


# Create your views here.
def index(request):
    product_list = Product.objects.all()
    content = {"products": product_list}
    return render(request, "catalog/index.html", content)


def contacts(request):
    if request.method == "POST":
        return render(request, "catalog/thanks.html")
    return render(request, "catalog/contacts.html")


def product(request, pk):
    product = Product.objects.get(id=pk)
    content = {"product": product}
    return render(request, "catalog/product.html", content)


def test(request):
    return render(request, "catalog/base.html")
