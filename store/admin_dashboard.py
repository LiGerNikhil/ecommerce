from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from store.models import Order, Product
from django.db.models import Sum

@staff_member_required
def admin_dashboard(request):
    order_count = Order.objects.count()
    total_sales = Order.objects.aggregate(total=Sum('total'))['total'] or 0
    product_count = Product.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    all_orders = Order.objects.order_by('-created_at')
    from store.models import Order as OrderModel
    status_choices = OrderModel.STATUS_CHOICES
    return render(request, 'admin_dashboard.html', {
        'order_count': order_count,
        'total_sales': total_sales,
        'product_count': product_count,
        'recent_orders': recent_orders,
        'all_orders': all_orders,
        'status_choices': status_choices,
    })
