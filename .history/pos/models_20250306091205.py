from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    datetimestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

