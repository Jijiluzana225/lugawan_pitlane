from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    
    path('', views.catalog, name='catalog'),  # New catalog page
    path('add-to-order/', views.add_to_order, name='add_to_order'),  # New URL for adding to order
    path('order-history/', views.order_history, name='order_history'),
    
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    
    path('other-income/', views.other_income_list, name='other_income_list'),
    path('other-income/add/', views.add_other_income, name='add_other_income'),
    path('other-income/edit/<int:income_id>/', views.edit_other_income, name='edit_other_income'),
    path('other-income/delete/<int:income_id>/', views.delete_other_income, name='delete_other_income'),
    
]
