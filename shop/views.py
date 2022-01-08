from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from shop.models import Product
from cart.forms import QuantityForm


def home_page(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	form = QuantityForm()
	product = get_object_or_404(Product, slug=slug)
	context = {'title':product.title, 'product':product, 'form':form, 'favorites':'favorites'}
	if request.user.likes.filter(id__in=str(product.id)):
		context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)


def search(request):
	query = request.GET.get('q')
	print(query)
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': products}
	return render(request, 'home_page.html', context)