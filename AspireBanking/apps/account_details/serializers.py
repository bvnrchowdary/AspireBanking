from rest_framework import serializers
from .models import AccountDetails

class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = '__all__'