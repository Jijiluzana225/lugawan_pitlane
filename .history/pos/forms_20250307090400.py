
from django import forms
from .models import *

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'datetimestamp']  # Add datetimestamp

        widgets = {
            'datetimestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }



class OtherIncomeForm(forms.ModelForm):
    class Meta:
        model = OtherIncome
        fields = ['description', 'amount', 'source']