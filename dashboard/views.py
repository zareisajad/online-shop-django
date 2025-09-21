from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.forms import modelformset_factory

from shop.models import Product, Shop, ProductImage
from accounts.models import User
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, EditProductForm, AddShopForm, ProductImageForm


def is_manager(user):
    try:
        if not user.is_manager:
            raise Http404
        return True
    except:
        raise Http404


@user_passes_test(is_manager)
@login_required
def products(request):
    try:
        user_shop = Shop.objects.get(owner=request.user)
    # Then get products from that shop
        products = Product.objects.filter(shop=user_shop)
        context = {'title':'Products' ,'products':products}
        return render(request, 'products.html', context)
    except Shop.DoesNotExist:
    # Handle case where user doesn't have a shop
        products = Product.objects.none()
        context = {'title':'Products' ,'products':products}
        return render(request, 'products.html', context)
    

@user_passes_test(is_manager)
@login_required
def add_shop(request):
    # Check if user already has a shop
    try:
        user_shop = Shop.objects.get(owner=request.user)
        # If user already has a shop, show message and redirect to products page
        messages.warning(request, 'You already have a shop! You cannot create another one.')
        return redirect('dashboard:products')
    except Shop.DoesNotExist:
        # User doesn't have a shop, proceed with shop creation
        if request.method == 'POST':
            form = AddShopForm(request.POST)
            if form.is_valid():
                user = request.user
                
                shop = form.save(commit=False)
                shop.owner = user
                shop.save()
                messages.success(request, 'Shop added Successfuly!')
                return redirect('dashboard:add_shop')
        else:
            form = AddShopForm()
        context = {'title':'Add shop', 'form':form}
        return render(request, 'add_shop.html', context)
    
@user_passes_test(is_manager)
@login_required
def add_product(request):
    ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3, max_num=10)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.shop = Shop.objects.get(owner=request.user)
            product.save()
            for image_form in formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()
            messages.success(request, 'Product added Successfully!')
            return redirect('dashboard:add_product')
    else:
        form = AddProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())
    context = {'title':'Add Product', 'form':form, 'formset': formset}
    return render(request, 'add_product.html', context)
    
@user_passes_test(is_manager)
@login_required
def delete_product(request, id):
    product = Product.objects.filter(id=id).delete()
    messages.success(request, 'product has been deleted!', 'success')
    return redirect('dashboard:products')


@user_passes_test(is_manager)
@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    # Check if the product belongs to the user's shop
    try:
        user_shop = Shop.objects.get(owner=request.user)
        if product.shop != user_shop:
            messages.error(request, "You can only edit products from your own shop!")
            return redirect('dashboard:products')
    except Shop.DoesNotExist:
        messages.error(request, "You don't have a shop!")
        return redirect('dashboard:add_shop')
    
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated', 'success')
            return redirect('dashboard:products')
    else:
        form = EditProductForm(instance=product)
    context = {'title': 'Edit Product', 'form':form}
    return render(request, 'edit_product.html', context)

@user_passes_test(is_manager)
@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added Successfuly!')
            return redirect('dashboard:add_category')
    else:
        form = AddCategoryForm()
    context = {'title':'Add Category', 'form':form}
    return render(request, 'add_category.html', context)


@user_passes_test(is_manager)
@login_required
def orders(request):
    orders = Order.objects.all()
    context = {'title':'Orders', 'orders':orders}
    return render(request, 'orders.html', context)


@user_passes_test(is_manager)
@login_required
def order_detail(request, id):
    order = Order.objects.filter(id=id).first()
    items = OrderItem.objects.filter(order=order).all()
    context = {'title':'order detail', 'items':items, 'order':order}
    return render(request, 'order_detail.html', context)


@user_passes_test(is_manager)
@login_required
def shop_detail(request):
    try:
        # Get the shop owned by the current user
        shop = Shop.objects.get(owner=request.user)
        
        if request.method == 'POST':
            form = AddShopForm(request.POST, instance=shop)
            if form.is_valid():
                form.save()
                messages.success(request, 'Shop details updated successfully!')
                return redirect('dashboard:shop_detail')
        else:
            form = AddShopForm(instance=shop)
            
        context = {
            'title': 'Shop Details',
            'form': form,
            'shop': shop
        }
        return render(request, 'edit_show_shop.html', context)
    except Shop.DoesNotExist:
        # If user doesn't have a shop, redirect to add shop page
        messages.warning(request, "You don't have a shop yet. Create one first!")
        return redirect('dashboard:add_shop')


