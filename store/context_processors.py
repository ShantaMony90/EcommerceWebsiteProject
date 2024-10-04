from store.models import *


def g_category(request):
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return context


def g_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).count()
    else:
        cart = 0

    context = {
        'cart': cart,
    }
    return context


def g_wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist = 0

    context = {
        'wishlist': wishlist,
    }
    return context
