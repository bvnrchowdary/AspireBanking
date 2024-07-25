import MySQLdb
from django.conf import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AspireBankingDataManager:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.connection = MySQLdb.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                passwd=settings.DATABASES['default']['PASSWORD'],
                db=settings.DATABASES['default']['NAME'],
                charset='utf8mb4'
            )
            self.cursor = self.connection.cursor()
            logger.info("Database connection established")
        except MySQLdb.Error as e:
            logger.exception("Error connecting to database")
            raise

    def close(self, commit=True):
        try:
            if self.connection:
                if commit:
                    self.connection.commit()
                if self.cursor:
                    self.cursor.close()
                    self.cursor = None
                self.connection.close()
                self.connection = None
                logger.info("Database connection closed")
        except MySQLdb.Error as e:
            logger.exception("Error closing database connection")

    def execute_query(self, query, params=None):
        try:
            if self.cursor is None or self.connection is None:
                self.connect()
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except MySQLdb.Error as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            if e.args[0] in (2006, 2013, 2014):  # MySQL server errors
                logger.info("Reconnecting to database")
                self.connect()
                self.cursor.execute(query, params)
                result = self.cursor.fetchall()
                return result
            return None
