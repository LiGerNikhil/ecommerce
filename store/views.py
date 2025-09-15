
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Order, OrderItem, Product, Category, Cart, CartItem
from django import forms

# Order detail view
@login_required
def order_detail_view(request, order_id):
	order = get_object_or_404(Order, pk=order_id, user=request.user)
	return render(request, 'store/order_detail.html', {'order': order})

# Shipping form for checkout
class ShippingForm(forms.Form):
	address = forms.CharField(max_length=255, label="Address")
	city = forms.CharField(max_length=100, label="City")
	postal_code = forms.CharField(max_length=20, label="Postal Code")
	country = forms.CharField(max_length=100, label="Country")


# Checkout: collect shipping details
@login_required
def checkout_view(request):
	cart, _ = Cart.objects.get_or_create(user=request.user)
	items = cart.items.select_related('product')
	total = sum(item.product.price * item.quantity for item in items)
	if not items.exists():
		messages.error(request, "Your cart is empty.")
		return redirect('cart')
	if request.method == 'POST':
		form = ShippingForm(request.POST)
		if form.is_valid():
			# Save shipping info in session and go to review
			request.session['shipping'] = form.cleaned_data
			return redirect('checkout_review')
	else:
		form = ShippingForm()
	return render(request, 'store/checkout.html', {'form': form, 'items': items, 'total': total})

# Checkout: review order
@login_required
def checkout_review_view(request):
	cart, _ = Cart.objects.get_or_create(user=request.user)
	items = cart.items.select_related('product')
	shipping = request.session.get('shipping')
	if not shipping or not items.exists():
		return redirect('checkout')
	total = sum(item.product.price * item.quantity for item in items)
	stock_errors = []
	for item in items:
		if item.quantity > item.product.stock:
			stock_errors.append(f"Not enough stock for {item.product.name} (Available: {item.product.stock}, In cart: {item.quantity})")
	if request.method == 'POST':
		if stock_errors:
			for err in stock_errors:
				messages.error(request, err)
			return redirect('checkout_review')
		# Create order and order items
		order = Order.objects.create(
			user=request.user,
			shipping_address=shipping['address'],
			shipping_city=shipping['city'],
			shipping_postal_code=shipping['postal_code'],
			shipping_country=shipping['country'],
			total=total
		)
		for item in items:
			OrderItem.objects.create(
				order=order,
				product=item.product,
				quantity=item.quantity,
				price=item.product.price
			)
			# Deduct stock
			item.product.stock -= item.quantity
			item.product.save()
		# Clear cart
		items.delete()
		messages.success(request, "Order placed successfully!")
		# Optionally clear shipping info
		request.session.pop('shipping', None)
		return redirect('order_success', order_id=order.id)
	return render(request, 'store/checkout_review.html', {'items': items, 'shipping': shipping, 'total': total, 'stock_errors': stock_errors})

# Checkout: order success
@login_required
def order_success_view(request, order_id):
	order = get_object_or_404(Order, pk=order_id, user=request.user)
	return render(request, 'store/order_success.html', {'order': order})

from django.db.models import Q
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator

# Cart views

@login_required
def cart_view(request):
	cart, _ = Cart.objects.get_or_create(user=request.user)
	items = cart.items.select_related('product')
	if request.method == 'POST':
		for item in items:
			quantity_str = request.POST.get(f'quantity_{item.id}')
			if quantity_str is not None:
				try:
					quantity = int(quantity_str)
					if quantity > 0:
						item.quantity = quantity
						item.save()
					else:
						item.delete()
				except ValueError:
					pass
		return redirect('cart')
	total = sum(item.product.price * item.quantity for item in items)
	return render(request, 'store/cart.html', {'cart': cart, 'items': items, 'total': total})


# Optional: Separate view for updating a single cart item quantity (AJAX or form action)
@login_required
def update_cart_item_quantity(request, item_id):
	cart = get_object_or_404(Cart, user=request.user)
	item = get_object_or_404(CartItem, pk=item_id, cart=cart)
	if request.method == 'POST':
		quantity_str = request.POST.get('quantity')
		try:
			quantity = int(quantity_str)
			if quantity > 0:
				item.quantity = quantity
				item.save()
			else:
				item.delete()
		except (ValueError, TypeError):
			pass
	return redirect('cart')

@login_required
def add_to_cart_view(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	cart, _ = Cart.objects.get_or_create(user=request.user)
	item, created = CartItem.objects.get_or_create(cart=cart, product=product)
	if not created:
		item.quantity += 1
		item.save()
	# If 'buynow' param is present, go directly to checkout
	if request.GET.get('buynow') == '1':
		return redirect('checkout')
	return redirect('cart')

@login_required
def remove_from_cart_view(request, item_id):
	cart = get_object_or_404(Cart, user=request.user)
	item = get_object_or_404(CartItem, pk=item_id, cart=cart)
	item.delete()
	return redirect('cart')

# List products by category
@login_required
def category_products_view(request, category_id):
	category = get_object_or_404(Category, pk=category_id)
	products = Product.objects.filter(category=category)
	categories = Category.objects.all()
	return render(request, 'store/product_list.html', {
		'products': products,
		'categories': categories,
		'selected_category': str(category_id),
		'search_query': '',
		'category_obj': category,
	})

@login_required
def product_detail_view(request, pk):
	product = get_object_or_404(Product, pk=pk)
	return render(request, 'store/product_detail.html', {'product': product})

@login_required
def product_list_view(request):
	query = request.GET.get('q', '')
	category_id = request.GET.get('category', '')
	products = Product.objects.all().order_by('-id')
	categories = Category.objects.all()
	if query:
		products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
	if category_id:
		products = products.filter(category_id=category_id)
	paginator = Paginator(products, 7)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'store/product_list.html', {
		'products': page_obj.object_list,
		'categories': categories,
		'selected_category': category_id,
		'search_query': query,
		'page_obj': page_obj,
		'paginator': paginator,
	})
from django import forms
from django.contrib import messages

# Create your views here.

def home_view(request):
		if request.user.is_authenticated:
			# Get cart and order count for dashboard
			cart, _ = Cart.objects.get_or_create(user=request.user)
			cart_items = cart.items.select_related('product')
			cart_total = sum(item.product.price * item.quantity for item in cart_items)
			order_count = Order.objects.filter(user=request.user).count()
			return render(request, 'store/home.html', {
				'dashboard': True,
				'cart_items': cart_items,
				'cart_total': cart_total,
				'order_count': order_count,
			})
		else:
			return render(request, 'store/home.html', {'dashboard': False})

def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Registration successful!')
			return redirect('profile')
	else:
		form = UserCreationForm()
	return render(request, 'store/register.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			messages.success(request, 'Login successful!')
			return redirect('profile')
	else:
		form = AuthenticationForm()
	return render(request, 'store/login.html', {'form': form})

def logout_view(request):
	logout(request)
	messages.info(request, 'Logged out successfully!')
	return redirect('login')


# Form for editing user profile
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['address', 'phone']

@login_required
def profile_view(request):
	user = request.user
	# Get or create user profile
	profile, created = UserProfile.objects.get_or_create(user=user)
	# Get or create cart and items
	cart, _ = Cart.objects.get_or_create(user=user)
	cart_items = cart.items.select_related('product')
	cart_total = sum(item.product.price * item.quantity for item in cart_items)
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile updated!')
			return redirect('profile')
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'store/profile.html', {
		'user': user,
		'form': form,
		'profile': profile,
		'cart_items': cart_items,
		'cart_total': cart_total,
	})

@login_required
def order_history_view(request):
	orders = Order.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'store/order_history.html', {'orders': orders})
