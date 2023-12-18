from django.contrib import admin
from blog.models import Record, Tag

# Register your models here.


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "views_count",
        "publicated",
    )
    list_filter = (
        "title",
        "publicated",
        "views_count",
    )
    search_fields = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "record",
    )
    list_filter = ("record",)
    search_fields = ("title", "record")
