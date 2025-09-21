from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from shop.models import CarBrand, Product, Category
from cart.forms import QuantityForm
from shop.models import CarModel, CarArticle


def categories_processor(request):
    categories = Category._default_manager.all()
    return {'categories': categories}


def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except django.core.paginator.PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj


def home_page(request):
	products = Product.objects.all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	shop = product.shop
	related_products = Product.objects.filter(category=product.category).all()[:5]
	context = {
		'title':product.title,
		'product':product,
	#	'favorites':'favorites',
		'related_products':related_products,
		'shop':shop	
	}
	#if request.user.likes.filter(id=product.id).first():
	#	context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)


#here is the product detail view add when want to add shoping app
"""
@login_required
def product_detail(request, slug):
	form = QuantityForm()
	product = get_object_or_404(Product, slug=slug)
	related_products = Product.objects.filter(category=product.category).all()[:5]
	context = {
		'title':product.title,
		'product':product,
		'form':form,
		'favorites':'favorites',
		'related_products':related_products
	}
	if request.user.likes.filter(id=product.id).first():
		context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)
"""

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
    # پارامترها مثل قبل…
    query = request.GET.get('q', '').strip()
    category_slugs = request.GET.getlist('category')
    brands        = request.GET.getlist('brand')
    price_min     = request.GET.get('price_min')
    price_max     = request.GET.get('price_max')
    in_stock      = request.GET.get('in_stock')
    car_model_ids = request.GET.getlist('car_model')
    

    qs = Product.objects.all()
    # اعمال فیلترها...
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    if category_slugs:
        qs = qs.filter(category__slug__in=category_slugs)
    if brands:
        qs = qs.filter(brand__in=brands)
    if price_min:
        qs = qs.filter(price__gte=price_min)
    if price_max:
        qs = qs.filter(price__lte=price_max)
    if in_stock == 'on':
        qs = qs.filter(stock__gt=0)
    if car_model_ids:
        qs = qs.filter(compatible_cars__id__in=car_model_ids)
    qs = qs.distinct()

    # برندها را یکتا و مرتب کنید
    brands_list = sorted(set([b.strip() for b in qs.values_list('brand', flat=True) if b]))

    print(brands_list)
    # صفحه‌بندی
    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': Category.objects.filter(is_sub=False),
        'brands': brands_list,
        'selected_categories': category_slugs,
        'selected_brands': brands,
        'price_min': price_min,
        'price_max': price_max,
        'in_stock': in_stock,
        'car_models': CarModel.objects.all(),
        'selected_car_models': car_model_ids,
    }

    # تشخیص AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        html = render(request, 'partials/_products_list.html', context).content.decode('utf-8')
        return JsonResponse({'html': html})

    return render(request, 'search.html', context)








def filter_by_category(request, slug):
    # Parse all filter parameters from request.GET, similar to 'search' function
    query = request.GET.get('q', '').strip()
    category_slugs = request.GET.getlist('category')
    brands_from_get = request.GET.getlist('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    in_stock = request.GET.get('in_stock')
    car_model_ids = request.GET.getlist('car_model')

    # Add the current category slug from the URL to selected_categories
    # This ensures the current category is marked as selected in the UI
    if slug not in category_slugs:
        category_slugs.append(slug)

    main_category = Category.objects.filter(slug=slug).first()

    if not main_category:
        # If the main category from the URL slug is not found, return an empty queryset
        qs = Product.objects.none()
    else:
        category_ids_for_filter = get_all_subcategory_ids(main_category)
        qs = Product.objects.filter(category_id__in=category_ids_for_filter)

    # Apply other filters from request.GET to the queryset (qs)
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    if brands_from_get:
        qs = qs.filter(brand__in=brands_from_get)
    if price_min:
        qs = qs.filter(price__gte=price_min)
    if price_max:
        qs = qs.filter(price__lte=price_max)
    if in_stock == 'on':
        qs = qs.filter(stock__gt=0)
    if car_model_ids:
        qs = qs.filter(compatible_cars__id__in=car_model_ids)

    qs = qs.distinct()

    # Generate brands_list from the final filtered queryset
    brands_list = sorted(set([b.strip() for b in qs.values_list('brand', flat=True) if b]))

    # Pagination
    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': Category.objects.filter(is_sub=False), # All main categories for filter options
        'brands': brands_list, # Brands relevant to the filtered products
        'selected_categories': category_slugs,
        'selected_brands': brands_from_get,
        'price_min': price_min,
        'price_max': price_max,
        'in_stock': in_stock,
        'car_models': CarModel.objects.all(), # All car models for filter options
        'selected_car_models': car_model_ids,
        'query': query, # Pass the query back to the template for input field
    }

    # Handle AJAX request
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        html = render(request, 'partials/_products_list.html', context).content.decode('utf-8')
        return JsonResponse({'html': html})

    return render(request, 'search.html', context)



def categories_processor(request):
	main_categories = Category.objects.filter(is_sub=False).all()
	return {'main_categories': main_categories}



def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        products = Product.objects.filter(title__icontains=query)[:10]
        results = list(products.values('slug', 'title'))
    return JsonResponse({'results': results})



def get_all_subcategory_ids(category):
    ids = [category.id]
    for sub in category.sub_categories.all():
        ids.extend(get_all_subcategory_ids(sub))
    return ids



def car_article_detail(request, slug):
    article = get_object_or_404(CarArticle, slug=slug, is_active=True)
    related_products = article.get_related_products()
    context = {
        'article': article,
        'related_products': related_products,
        'title': f"{article.car_brand.name} - {article.title}"
    }
    
    return render(request, 'car_article_detail.html', context)

def car_brand_articles(request, brand_slug):
    """نمایش مقالات یک برند خاص"""
    brand = get_object_or_404(CarBrand, Q(slug=brand_slug) | Q(name__iexact=brand_slug))
    articles = CarArticle.objects.filter(car_brand=brand, is_active=True)
    
    # صفحه‌بندی
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'brand': brand,
        'articles': page_obj,
        'title': f"مقالات {brand.name}"
    }
    
    return render(request, 'car_brand_articles.html', context)
