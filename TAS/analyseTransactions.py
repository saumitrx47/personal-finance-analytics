import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URI
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionAnalyser:
    def __init__(self, db_uri=DATABASE_URI):
        """Initialize the Transaction Analyser with database connection"""
        try:
            self.engine = create_engine(db_uri)
            self.connection = self.engine.connect()
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def calculate_monthly_spending_summary(self):
        """
        Calculate and store monthly spending summaries.
        Aggregates total spending and income by month.
        """
        try:
            query = """
            SELECT 
                strftime('%m-%Y', date) as year_month,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_spending,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE -amount END) as net_spending
            FROM transactions
            GROUP BY strftime('%Y-%m-01', date)
            ORDER BY year_month DESC
            """
            
            df = pd.read_sql(query, self.engine)
            
            df.to_sql('monthly_spending_summary', self.engine, if_exists='append', index=False)
            
            logger.info(f"Monthly spending summary calculated for {len(df)} months")
            return df
        except Exception as e:
            logger.error(f"Error calculating monthly spending summary: {e}")
            raise

    def calculate_category_wise_spending(self):
        """
        Calculate and store category-wise spending summaries.
        Aggregates spending by category and month.
        """
        try:
            query = """
            SELECT 
                category,
                SUM(ABS(amount)) as total_amount,
                COUNT(*) as transaction_count
            FROM transactions
            WHERE amount < 0 AND category IS NOT NULL
            GROUP BY category
            ORDER BY category asc
            """
            
            df = pd.read_sql(query, self.engine)
            
            df.to_sql('category_wise_spending', self.engine, if_exists='append', index=False)
            
            logger.info(f"Category-wise spending calculated for {len(df)} category-month combinations")
            return df
        except Exception as e:
            logger.error(f"Error calculating category-wise spending: {e}")
            raise

    def get_monthly_summary_report(self):
        """Retrieve the monthly spending summary report"""
        try:
            query = """
            SELECT * FROM monthly_spending_summary
            ORDER BY year_month DESC
            """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            logger.error(f"Error retrieving monthly summary: {e}")
            raise

    def get_category_spending_report(self, year_month=None):
        """Retrieve the category-wise spending report, optionally filtered by month"""
        try:
            if year_month:
                query = f"""
                SELECT * FROM category_wise_spending
                WHERE year_month = '{year_month}'
                ORDER BY total_amount DESC
                """
            else:
                query = """
                SELECT * FROM category_wise_spending
                ORDER BY year_month DESC, total_amount DESC
                """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            logger.error(f"Error retrieving category spending report: {e}")
            raise

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    analyser = TransactionAnalyser()
    
    try:
        # Calculate and store monthly spending summary
        logger.info("Calculating monthly spending summary...")
        monthly_summary = analyser.calculate_monthly_spending_summary()
        print("\nMonthly Spending Summary:")
        print(monthly_summary)
        
        # Calculate and store category-wise spending
        logger.info("Calculating category-wise spending...")
        category_summary = analyser.calculate_category_wise_spending()
        print("\nCategory-wise Spending:")
        print(category_summary)
        
    finally:
        analyser.close()
