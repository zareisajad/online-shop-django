from django.shortcuts import render, redirect
from shop.models import product
from django.contrib.auth.decorators import login_required
from .models import WishList
# Create your views here.

@login_required
def wish_list(request):
    """
    Display the user's wish list.
    """
    # Assuming 'products' is a queryset of products in the wish list
    wish_list_items = WishList.objects.filter(user=request.user)
    context = {
        'title': 'Wish List',
        'products': [item.product for item in wish_list_items],
    }
    return render(request, 'wishList:wish_list', context)





def remove_from_wish_list(request, product_id):
    """
    Remove a product from the user's wish list.
    """
    if request.method == 'POST':
        product = product.objects.get(id=product_id)
        WishList.objects.filter(user=request.user, product=product).delete()
        return redirect('wish_list')  # Redirect to the wish list view
    else:
        return render(request, 'wishList:remove_from_wish_list', {'product_id': product_id})
