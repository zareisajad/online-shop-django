from django import forms
from django.forms import ModelForm

from shop.models import Product, Category, Shop, ProductImage


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'image', 'title', 'description', 'price',
            'discount_price', 'color', 'compatible_cars', 'brand', 'manufacturer',
            'price_valid_until', 'has_warranty', 'warranty_months', 'is_active',
            'main_image'
        ]
        widgets = {
            'price_valid_until': forms.DateInput(attrs={'type': 'date'}),
            'compatible_cars': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
         sub_categories__isnull=True,
         sub_category__isnull=False
        )
        for visible in self.visible_fields():
            if visible.name not in ['has_warranty', 'is_active']:
                visible.field.widget.attrs['class'] = 'form-control'
            if visible.name in ['has_warranty', 'is_active']:
                visible.field.widget.attrs['class'] = 'form-check-input'

class AddShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'address', 'postal_code','description', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(AddShopForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'sub_category', 'is_sub']
    

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.fields['is_sub'].widget.attrs['class'] = 'form-check-input'
        self.fields['sub_category'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['class'] = 'form-control'


class EditProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'image', 'title', 'description', 'price',
            'compatible_cars', 'brand', 'manufacturer', 'price_valid_until',
            'has_warranty', 'warranty_months', 'main_image'
        ]
        widgets = {
            'price_valid_until': forms.DateInput(attrs={'type': 'date'}),
            'compatible_cars': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name not in ['has_warranty', 'is_active']:
                visible.field.widget.attrs['class'] = 'form-control'
            if visible.name in ['has_warranty', 'is_active']:
                visible.field.widget.attrs['class'] = 'form-check-input'



class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image','alt_text']