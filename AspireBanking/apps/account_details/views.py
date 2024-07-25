from rest_framework import viewsets
from .models import AccountDetails
from .serializers import AccountDetailsSerializer

class AccountDetailsViewSet(viewsets.ModelViewSet):
    queryset = AccountDetails.objects.all()
    serializer_class = AccountDetailsSerializer
