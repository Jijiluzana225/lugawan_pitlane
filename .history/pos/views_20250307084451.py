
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

    # Calculate total sales amount
    total_amount = sum(order.product.price * order.quantity for order in orders)

    context = {
        'orders': orders,
        'selected_date': selected_date,
        'total_amount': total_amount,
    }
    return render(request, 'pos/order_history.html', context)


from django.shortcuts import render
from .models import Expense, OtherIncome
from django.utils.timezone import localtime, now


def expense_list(request):
    local_now = localtime(now())
    expenses = Expense.objects.all().order_by('-datetimestamp')
    return render(request, 'pos/expenses.html', {'expenses': expenses, 'current_time': local_now})


def other_income_list(request):
    local_now = localtime(now())
    other_income = OtherIncome.objects.all().order_by('-datetimestamp')
    return render(request, 'pos/other_income.html', {'other_income': other_income, 'current_time': local_now})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.utils.timezone import localtime, now


def expense_list(request):
    local_now = localtime(now())
    expenses = Expense.objects.all().order_by('-datetimestamp')
    return render(request, 'pos/expenses.html', {'expenses': expenses, 'current_time': local_now})


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'pos/expense_form.html', {'form': form})


def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'pos/expense_form.html', {'form': form})


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
