from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from blog.models import Record
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from pytils.translit import slugify


class RecordCreateView(CreateView):
    model = Record
    fields = ("title", "content", "image")
    template_name = "blog/record_form.html"
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        new_record = form.save()
        new_record.slug = slugify(new_record.title)
        new_record.save()
        return super().form_valid(form)


class LikeRecord(SingleObjectMixin, View):
    model = Record
    http_method_names = ["post"]

    def post(self, request, *args, **kwards):
        record = self.get_object()
        record.attribute += 1
        record.save()
        return redirect(reverse("blog:list"))


class DislikeRecord(SingleObjectMixin, View):
    model = Record
    http_method_names = ["post"]

    def post(self, request, *args, **kwards):
        record = self.get_object()
        record.attribute -= 1
        record.save()
        return redirect(reverse("blog:list"))


class RecordUpdateView(UpdateView):
    model = Record
    fields = ("title", "content", "image")
    template_name = "blog/record_form.html"
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        new_record = form.save()
        new_record.slug = slugify(new_record.title)
        new_record.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy("blog:list")


class RecordListView(ListView):
    model = Record

    def get_queryset(self, *args, **kwards):
        queryset = super().get_queryset(*args, **kwards)
        queryset = queryset.filter(attribute__gte=0)
        return queryset


class RecordDetailView(DetailView):
    model = Record

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return super().get_object(queryset)
