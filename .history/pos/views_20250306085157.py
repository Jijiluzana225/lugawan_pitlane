from django.shortcuts import render
from .models import Category, Product
def menu(request):
    products = Product.objects.filter(available=True)
    return render(request, 'pos/menu.html', {'products': products})




def catalog(request):
    categories = Category.objects.prefetch_related('product_set').all()
    return render(request, 'pos/catalog.html', {'categories': categories})

from django.shortcuts import redirect, get_object_or_404
from .models import *

def add_to_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Get or create a pending order
        
        # Check if product is already in the order
        order_item, item_created = OrderItem.objects.get_or_create(
        
            product=product,
            defaults={'quantity': 1}
        )

        # If item exists, increase quantity
        if not item_created:
            order_item.quantity += 1
            order_item.save()

    return redirect('catalog')
