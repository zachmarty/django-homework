from django.urls import path
from catalog.views import *
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", index, name="index"),
    path("contacts", contacts, name="contacts"),
    path("test", test),
    path("product/<int:pk>", product, name="product"),
]
