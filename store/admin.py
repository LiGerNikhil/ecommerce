from django.contrib import admin
from .models import Category, Product, Order, OrderItem
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'created_at', 'updated_at', 'total')
	list_filter = ('status', 'created_at', 'user')
	search_fields = ('id', 'user__username', 'shipping_address', 'shipping_city', 'shipping_postal_code', 'shipping_country')
	inlines = [OrderItemInline]
	actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']

	def mark_as_processing(self, request, queryset):
		queryset.update(status='processing')
	mark_as_processing.short_description = "Mark selected orders as Processing"

	def mark_as_shipped(self, request, queryset):
		queryset.update(status='shipped')
	mark_as_shipped.short_description = "Mark selected orders as Shipped"

	def mark_as_delivered(self, request, queryset):
		queryset.update(status='delivered')
	mark_as_delivered.short_description = "Mark selected orders as Delivered"

	def mark_as_cancelled(self, request, queryset):
		queryset.update(status='cancelled')
	mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'product', 'quantity', 'price')
	search_fields = ('order__id', 'product__name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'stock', 'created_at')
	list_filter = ('category',)
	search_fields = ('name', 'description')
