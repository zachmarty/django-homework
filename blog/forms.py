from django import forms
from blog.models import Record, Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("title", "description")

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ("title", "content", "image")

    



