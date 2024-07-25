from django.db import models


class TransactionType(models.TextChoices):
    WITHDRAW = 'WITHDRAW', 'Withdraw'
    DEPOSIT = 'DEPOSIT', 'Deposit'

# Create your models here.
class Transaction(models.Model):
    Id = models.AutoField(primary_key=True)
    TransactionDate = models.DateTimeField(auto_now_add=True)
    Amount = models.FloatField()
    Description = models.TextField()
    TransactionType = models.CharField(max_length=25, choices=TransactionType.choices)
    AccountId = models.BigIntegerField()

    def __str__(self):
        return f"Transaction {self.Id} - {self.TransactionType}"
    class Meta:
        db_table = 'Transaction'
        managed = False
