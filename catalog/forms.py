from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

    def clean_name(self):
        cleaned_data = self.cleaned_data["name"]
        ban_words = [
            "казино",
            "криптовалюса",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in ban_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Запретка в названии продукта")
            
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data["description"]
        ban_words = [
            "казино",
            "криптовалюса",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in ban_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Запретка в описании продукта")
            
        return cleaned_data
    
class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ("v_name",)
