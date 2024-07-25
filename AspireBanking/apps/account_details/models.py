from django.db import models


class AccountTypes(models.TextChoices):
    SAVING = 'SAVING', 'Saving'
    CURRENT = 'CURRENT', 'Current'

# Create your models here.
class AccountDetails(models.Model):
    Id = models.AutoField(primary_key=True)
    AccountNumber = models.CharField(max_length=10, unique=True)
    AccountHolderName = models.CharField(max_length=50)
    AccountType = models.CharField(max_length=10, choices=AccountTypes.choices)
    Balance = models.FloatField()
    LastUpdateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account Details - {self.AccountHolderName} - {self.AccountNumber}"
    
    class Meta:
        db_table = 'AccountDetails'
        managed = False