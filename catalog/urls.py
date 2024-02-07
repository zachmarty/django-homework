from django.urls import path
from catalog.views import *
from catalog.apps import CatalogConfig
from django.conf import settings
from django.conf.urls.static import static

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("contacts", ProductContacts.as_view(), name="contacts"),
    path("view/<int:pk>", ProductDetailView.as_view(), name="view"),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name = 'edit'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name= 'delete'),
    path('thanks', ProductThanks.as_view(), name = 'thanks')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
