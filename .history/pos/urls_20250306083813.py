from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('orders/', views.order_summary, name='orders'),
    path('catalog/', views.catalog, name='catalog'),  # New catalog page
]
