
from django.db import models
from django.conf import settings

class Cart(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Cart for {self.user.username}"

class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('Product', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"
from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# Add additional fields as needed, e.g. address, phone, etc.
	address = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return self.user.username


# Category model
class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

# Product model
class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
	image = models.ImageField(upload_to='products/', blank=True, null=True)
	stock = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


# Order model

class Order(models.Model):
	STATUS_CHOICES = [
		("pending", "Pending"),
		("processing", "Processing"),
		("shipped", "Shipped"),
		("delivered", "Delivered"),
		("cancelled", "Cancelled"),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
	shipping_address = models.CharField(max_length=255, blank=True, null=True)
	shipping_city = models.CharField(max_length=100, blank=True, null=True)
	shipping_postal_code = models.CharField(max_length=20, blank=True, null=True)
	shipping_country = models.CharField(max_length=100, blank=True, null=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def __str__(self):
		return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.quantity} x {self.product.name}"
