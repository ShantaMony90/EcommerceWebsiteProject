from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Banner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    product_name = models.CharField(max_length=400, null=True, blank=True)
    price = models.CharField(max_length=14)
    dis_price = models.CharField(max_length=14, null=True, blank=True)
    brand = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Banner"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    img = models.ImageField(
        upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Brands(models.Model):
    name = models.CharField(max_length=50, null=False)
    img = models.ImageField(upload_to='category_images/', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = ("Brands")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ProductImage')
    regular_price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    descriptions = models.TextField()
    additional_descriptions = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.name


class DashboardInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.TextField(max_length=100)
    email = models.EmailField(default='')
    password = models.CharField(max_length=8)
    new_password = models.CharField(max_length=8, default='')
    confirm_password = models.CharField(max_length=8, default='')

    def __str__(self):
        return self.first_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name} "


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.product.name} - {self.quantity}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adddress = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    delivery_area = models.CharField(max_length=20, choices=[(
        'inside_dhaka', 'Inside Dhaka'), ('outside_dhaka', 'Outside Dhaka')])

    def __str__(self):
        return f"Order {self.user.username} - {self.address}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
