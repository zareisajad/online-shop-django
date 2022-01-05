from django import forms
from django.forms import ModelForm

from shop.models import Product


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title','description', 'price']

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'