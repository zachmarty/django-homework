from django.urls import path
from blog.views import *
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("create/", RecordCreateView.as_view(), name="create"),
    path("", RecordListView.as_view(), name="list"),
    path("edit/<int:pk>", RecordUpdateView.as_view(), name="edit"),
    path("view/<int:pk>", RecordDetailView.as_view(), name="view"),
    path("delete/<int:pk>", RecordDeleteView.as_view(), name="delete"),
    path("like/<int:pk>", add_attr, name="like"),
    path("dislike/<int:pk>", les_attr, name="dislike"),
]
