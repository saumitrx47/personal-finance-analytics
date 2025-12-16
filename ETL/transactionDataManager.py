import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError  
import logging
from config import DATABASE_URI
from ETL.dataTransformer import add_category_column
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionDataManager:
    def __init__(self, db_uri=DATABASE_URI):
        db_file = "personal_finance.db"

        if os.path.exists(db_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"personal_finance_{timestamp}.db"
            os.rename(db_file, backup_file)
            logger.info(f"Renamed existing DB to {backup_file}")
        
        self.engine = create_engine(db_uri)

    def load_data(self, file_path):
        try:
            df = pd.read_csv(file_path, header=0, parse_dates=['date'])
            logger.info(f"Loaded data from {file_path} with {len(df)} records.")
            return df
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            raise
    
    def save_data(self, df, table_name='transactions'):
        try:
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            logger.info(f"Saved {len(df)} records to table {table_name}.")
        except SQLAlchemyError as e:
            logger.error(f"Error saving data to table {table_name}: {e}")
            raise

    def process_and_store(self, file_path):
        df = self.load_data(file_path)
        logger.info("Transforming data by adding category column.")
        df = add_category_column(df) 
        self.save_data(df)
        logger.info("Data processing and storage completed successfully.")
        return df

if __name__ == "__main__":
    manager = TransactionDataManager()
    test_file_path = 'DATA/sampleData.csv'
    manager.process_and_store(test_file_path)
