from cart.utils.cart import Cart


def return_cart(request):
    cart = len(list(Cart(request)))
    return {'cart_count': cart}