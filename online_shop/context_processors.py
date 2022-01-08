from cart.utils.cart import Cart
from shop.models import Category


def return_cart(request):
    cart = len(list(Cart(request)))
    return {'cart_count': cart}


def return_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}