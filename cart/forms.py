from django import forms


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(label='',
        min_value=1, max_value=9, widget=forms.NumberInput(
            attrs={'class': 'form-control mt-1','placeholder': 'quantity'}
        )
    )

#class VoucherForm(forms.Form):
#    voucher = forms.TextInput(label='',
#        widget=forms.TextInput(
#            attrs={'class': 'form-control mt-1','placeholder': 'voucher code'}
#        )
#    )