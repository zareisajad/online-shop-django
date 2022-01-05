from django.shortcuts import render

from shop.models import Product


def home_page(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	return render(request, 'home_page.html')