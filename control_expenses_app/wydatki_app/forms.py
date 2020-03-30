from django.forms import ModelForm
from .models import Expense

'''
class NewExpenseForm(forms.Form):
    CATEGORIES = [
        ('1', 'Produkty spożywcze'),
        ('2', 'Chemia gospodarcza'),
        ('3', 'Ubrania'),
        ('4', 'Rozrywka'),
        ('5', 'Alkohol'),
        ('6', 'Rozwój osobisty'),
        ('7', 'Suplementy'),
        ('8', 'Inne')
    ]
    name = forms.CharField(label="Nazwa:", max_length=100)
    price = forms.FloatField(label="Cena:")
    category = forms.ChoiceField(label="Kategoria:", choices=CATEGORIES)
    purchase_date = forms.DateField(label="Data zakupu:")
'''

class NewExpenseModelForm(ModelForm):

    class Meta:
        model = Expense
        fields = '__all__'
