from django.forms import ModelForm, Textarea, DateInput
from .models import Expense


class NewExpenseModelForm(ModelForm):

    class Meta:
        model = Expense
        fields = '__all__'
        labels = {'name': 'Nazwa', 'price': 'Cena (PLN)', 'category': 'Kategoria', 'purchase_date': 'Data zakupu'}
        widgets = {'purchase_date': DateInput(attrs={'type': 'date'})}