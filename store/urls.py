
from django.urls import path
from . import views

urlpatterns = [
    # User authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # User profile
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.order_history_view, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    # Product catalog
    path('products/', views.product_list_view, name='product_list'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('category/<int:category_id>/', views.category_products_view, name='category_products'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),

    # Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/review/', views.checkout_review_view, name='checkout_review'),
    path('checkout/success/<int:order_id>/', views.order_success_view, name='order_success'),
]
