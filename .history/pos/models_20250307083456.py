from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def total_ordered_today(self):
        from django.db.models import Sum
        from datetime import date

        today = date.today()
        total = OrderItem.objects.filter(
            product=self,
            datetimestamp__date=today
        ).aggregate(Sum('quantity'))['quantity__sum']

        return total or 0


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    datetimestamp = models.DateTimeField(default=now)  # New field

    def __str__(self):
        return f"{self.quantity} x {self.product.name} at {self.datetimestamp}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('supplies', 'Supplies'),
        ('utilities', 'Utilities'),
        ('rent', 'Rent'),
        ('salary', 'Salary'),
        ('others', 'Others'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    datetimestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.description} - ₱{self.amount} on {self.datetimestamp}"


# New Other Income model
class OtherIncome(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100, blank=True, null=True)  # Optional source
    datetimestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.description} - ₱{self.amount} on {self.datetimestamp}"