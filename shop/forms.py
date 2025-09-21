from django import forms
from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'address', 'postal_code', 'description', 'phone_number']
        exclude = ['owner', 'date_created', 'admins'] 