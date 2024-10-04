import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    banner = Banner.objects.all()
    product = Product.objects.all().order_by('?')
    brand = Brands.objects.all()
    context = {
        'banner': banner,
        'product': product,
        'brand': brand,
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def dashboard_page(request):
    if request.method == 'POST':
        form_2 = DashboardForm(request.POST)
        if form_2.is_valid():
            form_2.save()
            return redirect('dashboard')
    else:
        form_2 = DashboardForm()
    return render(request, 'dashboard.html', {'form_2': form_2})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)

    related_products = Product.objects.filter(
        category=product.category).exclude(id=product.pk).order_by('?')[0:11]

    context = {
        'product': product,
        'related_products': related_products
    }

    return render(request, 'product_detail.html', context)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required(login_url='login')
def increment_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required(login_url='login')
def decrement_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.regular_price *
                item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required(login_url="login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = Wishlist.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('wishlist')


def remove_from_wishlist(request, product_id):
    wishlist_item = get_object_or_404(
        Wishlist, product__id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')


@login_required(login_url='login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.regular_price *
                          item.quantity for item in cart_items)

        # Handle shipping address
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        delivery_area = request.POST.get('delivery_area')

        # Add delivery charge
        if delivery_area == 'inside_dhaka':
            delivery_charge = 60
        else:
            delivery_charge = 120

        # Add the delivery charge to the total price
        total_price += delivery_charge

        # Create order and order items
        order = Order.objects.create(
            user=request.user, total_price=total_price)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.regular_price
            )

        # Clear the cart
        cart_items.delete()

        return redirect('payment', order_id=order.id)

    # Calculate total price for GET requests
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.regular_price *
                      item.quantity for item in cart_items)

    # Prepare context for the template
    delivery_area_charge = {
        'inside_dhaka': 60,
        'outside_dhaka': 120
    }

    context = {
        'total_price': total_price,
        'delivery_area_charge': delivery_area_charge,
    }

    return render(request, 'checkout.html', context)


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        transaction_id = str(uuid.uuid4())

        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            payment_method=request.POST.get('payment_method'),
            transaction_id=transaction_id,
            status='completed'
        )

        order.status = "processing"
        order.save()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'payment.html', {'order': order})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})
