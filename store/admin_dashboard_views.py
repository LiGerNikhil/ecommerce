from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Order, Product
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.urls import reverse

@staff_member_required
def admin_dashboard(request):
    order_count = Order.objects.count()
    total_sales = Order.objects.aggregate(total=Sum('total'))['total'] or 0
    product_count = Product.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    all_orders = Order.objects.order_by('-created_at')
    return render(request, 'admin_dashboard.html', {
        'order_count': order_count,
        'total_sales': total_sales,
        'product_count': product_count,
        'recent_orders': recent_orders,
        'all_orders': all_orders,
    })

@staff_member_required
@require_POST
def admin_update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
    return redirect(reverse('admin-dashboard'))
