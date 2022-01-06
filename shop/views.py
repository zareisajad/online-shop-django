from django.shortcuts import render

from shop.models import Product


def home_page(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	product = Product.objects.filter(slug=slug).first()
	context = {'title':product.title, 'product':product}
	return render(request, 'product_detail.html', context)