from django.shortcuts import render
from .models import Category, Product
def menu(request):
    products = Product.objects.filter(available=True)
    return render(request, 'pos/menu.html', {'products': products})




def catalog(request):
    categories = Category.objects.prefetch_related('product_set').all()
    return render(request, 'pos/catalog.html', {'categories': categories})


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
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date
from .models import Product, OrderItem

def menu(request):
    categories = Product.objects.select_related('category').all()

    # Calculate total sales for the day
    today = date.today()
    total_sales = OrderItem.objects.filter(
        datetimestamp__date=today
    ).aggregate(total=Sum('product__price', field='product__price * quantity'))['total'] or 0

    return render(request, 'pos/catalog.html', {
        'categories': categories,
        'total_sales': total_sales
    })
