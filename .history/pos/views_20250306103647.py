from django.shortcuts import render
from .models import Category, Product




def catalog(request):
    
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
    categories = Category.objects.prefetch_related('product_set').all()
    
    todays_orders = OrderItem.objects.filter(
        datetimestamp__date=today
    ).select_related('product').order_by('-datetimestamp')
    
    return render(request, 'pos/catalog.html', {'categories': categories,'total_sales': total_sales,'todays_orders': todays_orders})


from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
from .models import Product, OrderItem

def add_to_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Get quantity, default to 1 if missing
        product = get_object_or_404(Product, id=product_id)

        # Always create a new OrderItem record with the provided quantity
        OrderItem.objects.create(
            product=product,
            quantity=quantity,
            datetimestamp=now()
        )

    return redirect('catalog')


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

    context = {
        'orders': orders,
        'selected_date': selected_date,
    }
    return render(request, 'pos/order_history.html', context)
