from django.contrib import admin
from catalog.models import Category, Product, Version

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "user")
    list_filter = ("category", "user")
    search_fields = ("name", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = ("name",)
    search_fields = ("name", "description")


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "v_number", "v_name", "current", "add_date")
    list_filter = ("v_name", "v_number", "current", "add_date")
    search_fields = ("product",)
