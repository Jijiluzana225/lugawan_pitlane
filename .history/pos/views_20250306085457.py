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
        product = get_object_or_404(Product, id=product_id)

        # Always create a new OrderItem record
        OrderItem.objects.create(
            product=product,
            quantity=1,  # You can adjust this if quantity selection is needed
            datetimestamp=now()  # Use current timestamp
        )

    return redirect('catalog')

