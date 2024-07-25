import pandas as pd
from rest_framework import viewsets, status
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.decorators import action
import logging
from rest_framework.response import Response
import datamanager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['POST'], url_path='upload')
    def upload_transactions(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return Response({"error": "Invalid CSV file"}, status=status.HTTP_400_BAD_REQUEST)

        transactions = []
        for _, row in df.iterrows():
            transaction_data = {
                'TransactionDate': row['TransactionDate'],
                'Amount': row['Amount'],
                'Description': row['Description'],
                'TransactionType': row['TransactionType'],
                'AccountId': row['AccountId']
            }
            serializer = TransactionSerializer(data=transaction_data)
            if serializer.is_valid():
                transactions.append(serializer.save())
            else:
                logger.error(f"Validation error: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Transactions uploaded successfully"}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET'], url_path='search')
    def search_transaction(self, request):
        # Extract query parameters
        transaction_type = self.request.query_params.get('TransactionType', None)
        account_number = self.request.query_params.get('AccountNumber', None)
        account_holder_name = self.request.query_params.get('AccountHolderName', None)
        account_type = self.request.query_params.get('AccountType', None)

        # Initialize database manager
        manager = datamanager.AspireBankingDataManager()

        # Prepare the parameters for the stored procedure
        params = (
            transaction_type,
            account_number,
            account_holder_name,
            account_type
        )

        # Define the query to call the stored procedure
        query = """
        CALL TransactionSearch(%s, %s, %s, %s)
        """
        
        try:
            # Execute the stored procedure and fetch results
            result = manager.execute_query(query, params)

            # Convert the result to a list of dictionaries
            columns = [desc[0] for desc in manager.cursor.description]
            data = [dict(zip(columns, row)) for row in result]

            return Response(data)
        
        except Exception as e:
            logger.error(f"Error executing stored procedure: {e}")
            return Response({"error": "An error occurred while processing your request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Ensure database connection is closed
            manager.close()
