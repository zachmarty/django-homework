from typing import Any
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from blog.models import Record, Tag
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from pytils.translit import slugify
from blog.forms import RecordForm, TagForm
from django.forms import inlineformset_factory

class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        new_record = form.save()
        new_record.slug = slugify(new_record.title)
        new_record.save()
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwards):
        context_data = super().get_context_data(**kwards)
        RecordFormset = inlineformset_factory(Record, Tag, form=TagForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = RecordFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = RecordFormset(instance=self.object)
        return context_data
    


class LikeRecord(SingleObjectMixin, View):
    model = Record
    http_method_names = ["post"]

    def post(self, request, *args, **kwards):
        record = self.get_object()
        record.likes_count += 1
        record.save()
        return redirect(reverse("blog:view", kwargs={'pk': record.pk}))


class DislikeRecord(SingleObjectMixin, View):
    model = Record
    http_method_names = ["post"]

    def post(self, request, *args, **kwards):
        record = self.get_object()
        record.dislikes_count += 1
        record.save()
        return redirect(reverse("blog:view", kwargs={'pk': record.pk}))


class RecordUpdateView(UpdateView):
    model = Record
    form_class = RecordForm

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        new_record = form.save()
        new_record.slug = slugify(new_record.title)
        new_record.save()
        self.object = form.save()
        if formset.is_valid():      
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwards):
        context_data = super().get_context_data(**kwards)
        RecordFormset = inlineformset_factory(Record, Tag, form=TagForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = RecordFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = RecordFormset(instance=self.object)
        return context_data

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy("blog:list")


class RecordListView(ListView):
    model = Record

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publicated=True)
        return queryset


class RecordDetailView(DetailView):
    model = Record

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.filter(record = self.object)
        context['tags'] = tags
        return context
