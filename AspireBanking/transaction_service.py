import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import datamanager
import time
import os
import django
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AspireBanking.settings')

# Setup Django
django.setup()

class TransactionService:
    def __init__(self):
        self.manager = datamanager.AspireBankingDataManager()

    def fetch_account_ids(self):
        query = "SELECT AccountNumber FROM AccountDetails"
        result = self.manager.execute_query(query)
        # Convert result to DataFrame
        df = pd.DataFrame(result, columns=['AccountNumber'])
        if df.empty:
            logger.error("No account numbers found in the AccountDetails table.")
            return []
        return df['AccountNumber'].tolist()

    def generate_data(self, num_records):
        # Fetch existing account IDs
        account_ids = self.fetch_account_ids()
        if not account_ids:
            return pd.DataFrame()  # Return an empty DataFrame if no account IDs are found

        # Generate random dates within the last year
        start_date = datetime.now() - timedelta(days=365)
        date_range = [start_date + timedelta(days=random.uniform(0, 365)) for _ in range(num_records)]

        # Generate random amounts between 10 and 10000
        amounts = np.random.uniform(10, 10000, num_records).round(2)

        # Sample descriptions
        descriptions = ['Grocery', 'Salary', 'Rent', 'Utilities', 'Entertainment', 'Insurance', 'Dining', 'Travel']

        # Mapping descriptions to transaction types
        description_to_type = {
            'Grocery': 'WITHDRAW',
            'Rent': 'WITHDRAW',
            'Utilities': 'WITHDRAW',
            'Entertainment': 'WITHDRAW',
            'Insurance': 'WITHDRAW',
            'Dining': 'WITHDRAW',
            'Travel': 'WITHDRAW',
            'Salary': 'DEPOSIT'
        }

        # Randomly select account IDs from the fetched list
        account_ids_selected = [random.choice(account_ids) for _ in range(num_records)]

        # Create the DataFrame
        data = {
            'TransactionDate': date_range,
            'Amount': amounts,
            'Description': np.random.choice(descriptions, num_records),
            'TransactionType': [description_to_type[desc] for desc in np.random.choice(descriptions, num_records)],
            'AccountId': account_ids_selected
        }
        df = pd.DataFrame(data)
        return df

    def save_to_database(self, df):
        for index, row in df.iterrows():
            query = """
            INSERT INTO Transaction (TransactionDate, Amount, Description, TransactionType, AccountId)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (row['TransactionDate'], row['Amount'], row['Description'], row['TransactionType'], row['AccountId'])
            self.manager.execute_query(query, params)
            logger.info(f"Inserted transaction: {params}")

    def run(self, num_records):
        start_time = time.time()
        df = self.generate_data(num_records)
        if not df.empty:
            self.save_to_database(df)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution time: {execution_time} seconds")

    def start_service(self, interval_minutes=2):
        while True:
            self.run(1000)  # Generate and save 1,000 records
            logger.info(f"Service executed at {datetime.now()}")
            time.sleep(interval_minutes * 60)  # Sleep for the specified interval

# Usage example
if __name__ == "__main__":
    service = TransactionService()
    service.start_service(2)  # Run the service every 2 minutes
