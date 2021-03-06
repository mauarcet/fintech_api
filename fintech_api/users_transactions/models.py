from django.db import models
import uuid


class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=30)
    age = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['created_at']

class Transaction(models.Model):
    TransactionType = models.TextChoices('TransactionType', 'inflow outflow')
    reference = models.CharField(primary_key=True, max_length=20)
    account = models.CharField(max_length=15)
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    type = models.CharField(blank=True, choices=TransactionType.choices ,max_length=15)
    category = models.CharField(max_length=15)
    user_id = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )