from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    
    path('', views.catalog, name='catalog'),  # New catalog page
    path('add-to-order/', views.add_to_order, name='add_to_order'),  # New URL for adding to order
    path('order-history/', views.order_history, name='order_history'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('other-income/', views.other_income_list, name='other_income_list'),
    
    
]
