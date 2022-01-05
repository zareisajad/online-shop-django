from django.shortcuts import render, redirect

from shop.models import Product
from .forms import AddProductForm


def products(request):
    products = Product.objects.all()
    context = {'title':'Products' ,'products':products}
    return render(request, 'products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:add_product')
    else:
        form = AddProductForm()
    context = {'title':'Add Product', 'form':form}
    return render(request, 'add_product.html', context)

