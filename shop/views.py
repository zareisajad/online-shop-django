from django.shortcuts import render

from shop.models import Product
from cart.forms import QuantityForm


def home_page(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	form = QuantityForm()
	product = Product.objects.filter(slug=slug).first()
	context = {'title':product.title, 'product':product, 'form':form}
	return render(request, 'product_detail.html', context)