from django.contrib import admin
from blog.models import Record

# Register your models here.


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "views_count",
        "attribute",
    )
    list_filter = (
        "title",
        "attribute",
        "views_count",
    )
    search_fields = ("title",)
