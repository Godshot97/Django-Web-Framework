from django.db import models

from login_app.models import Account


class Expense(models.Model):
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
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=1, choices=CATEGORIES)
    purchase_date = models.DateField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)


    def __str__(self):
        return self.get_category_display() + " - " + self.name
