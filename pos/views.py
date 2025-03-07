
from django.shortcuts import render
from django.db.models import Sum, F
from django.utils.timezone import activate, localtime, now
from datetime import date
from .models import Product, OrderItem, Category

def catalog(request):
    # Set timezone to Philippines
    activate('Asia/Manila')
    
    # Get today's date in local timezone
    local_now = localtime(now())
    local_today = local_now.date()

    # Calculate total sales for the day from OrderItem model
    total_sales = OrderItem.objects.filter(
        datetimestamp__date=local_today
    ).annotate(
        total_price=F('product__price') * F('quantity')  # Calculate total price per item
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    # Fetch categories
    categories = Category.objects.prefetch_related('product_set').all()

    # Fetch today's orders, ensuring timestamps are converted to local time
    todays_orders = OrderItem.objects.filter(
        datetimestamp__date=local_today
    ).select_related('product').order_by('-datetimestamp')

    return render(request, 'pos/catalog.html', {
        'categories': categories,
        'total_sales': total_sales,
        'todays_orders': todays_orders
    })



from django.shortcuts import render
from django.db.models import Sum, F
from django.utils.timezone import now
from datetime import date
from .models import Product, OrderItem

def menu(request):
    categories = Product.objects.select_related('category').all()

    # Calculate total sales for the day from OrderItem model
    today = date.today()
    total_sales = OrderItem.objects.filter(
        datetimestamp__date=today
    ).annotate(
        total_price=F('product__price') * F('quantity')  # Calculate total price per item
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    return render(request, 'pos/catalog.html', {
        'categories': categories,
        'total_sales': total_sales
    })

from django.shortcuts import render
from django.utils.timezone import now
from .models import OrderItem

def order_history(request):
    # Get date from request (if provided), otherwise default to today
    selected_date = request.GET.get('date', now().date())

    # Filter and order OrderItem by the selected date and newest first
    orders = OrderItem.objects.filter(datetimestamp__date=selected_date).order_by('-datetimestamp')

    # Calculate total sales amount
    total_amount = sum(order.product.price * order.quantity for order in orders)

    context = {
        'orders': orders,
        'selected_date': selected_date,
        'total_amount': total_amount,
    }
    return render(request, 'pos/order_history.html', context)
