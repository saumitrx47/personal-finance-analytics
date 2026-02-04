import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from config import DATABASE_URI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinanceVisualizer:
    def __init__(self, db_uri=DATABASE_URI):
        """Initialize the visualizer with database connection"""
        try:
            self.engine = create_engine(db_uri)
            logger.info("Database connection established for visualization")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def visualize_transactions_table(self):
        """Display transactions as a formatted table"""
        try:
            query = """
            SELECT 
                date,
                description,
                category,
                amount,
                balance
            FROM transactions
            ORDER BY date DESC
            LIMIT 50
            """
            
            df = pd.read_sql(query, self.engine)
            
            if df.empty:
                logger.warning("No transactions found in database")
                return
            
            # Format the dataframe for display
            df['amount'] = df['amount'].apply(lambda x: f"${x:.2f}")
            df['balance'] = df['balance'].apply(lambda x: f"${x:.2f}")
            
            # Create figure and display table
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.axis('tight')
            ax.axis('off')
            
            table = ax.table(
                cellText=df.values,
                colLabels=df.columns,
                cellLoc='center',
                loc='center',
                colWidths=[0.08, 0.12, 0.25, 0.12, 0.12, 0.12]
            )
            
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1, 2)
            
            # Style header
            for i in range(len(df.columns)):
                table[(0, i)].set_facecolor('#40466e')
                table[(0, i)].set_text_props(weight='bold', color='white')
            
            # Alternate row colors
            for i in range(1, len(df) + 1):
                for j in range(len(df.columns)):
                    if i % 2 == 0:
                        table[(i, j)].set_facecolor('#f0f0f0')
                    else:
                        table[(i, j)].set_facecolor('white')
            
            plt.title('Recent Transactions (Last 50)', fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            plt.savefig('visualizations/transactions_table.png', dpi=300, bbox_inches='tight')
            logger.info("Transactions table visualization saved to visualizations/transactions_table.png")
            plt.show()
            
        except Exception as e:
            logger.error(f"Error visualizing transactions table: {e}")
            raise

    def visualize_monthly_spending_pie(self):
        """Display monthly spending summary as pie charts"""
        try:
            query = """
            SELECT 
                year_month,
                total_spending,
                total_income
            FROM monthly_spending_summary
            ORDER BY year_month DESC
            LIMIT 12
            """
            
            df = pd.read_sql(query, self.engine)
            
            if df.empty:
                logger.warning("No monthly spending summary found in database")
                return
            
            # Create subplots for spending and income
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Spending bar chart
            colors_spending = plt.cm.Reds(range(len(df)))
            ax1.bar(
                range(len(df)),
                df['total_spending'],
                color=colors_spending,
                edgecolor='black',
                linewidth=1.2
            )
            ax1.set_xticks(range(len(df)))
            ax1.set_xticklabels(df['year_month'], rotation=45, ha='right')
            ax1.set_ylabel('Amount ($)', fontsize=11, fontweight='bold')
            ax1.set_title('Monthly Spending Distribution', fontsize=14, fontweight='bold')
            ax1.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Income bar chart
            colors_income = plt.cm.Greens(range(len(df)))
            ax2.bar(
                range(len(df)),
                df['total_income'],
                color=colors_income,
                edgecolor='black',
                linewidth=1.2
            )
            ax2.set_xticks(range(len(df)))
            ax2.set_xticklabels(df['year_month'], rotation=45, ha='right')
            ax2.set_ylabel('Amount ($)', fontsize=11, fontweight='bold')
            ax2.set_title('Monthly Income Distribution', fontsize=14, fontweight='bold')
            ax2.grid(axis='y', alpha=0.3, linestyle='--')
            
            plt.suptitle('Monthly Spending Summary', fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            plt.savefig('visualizations/monthly_spending_pie.png', dpi=300, bbox_inches='tight')
            logger.info("Monthly spending pie chart saved to visualizations/monthly_spending_pie.png")
            plt.show()
            
        except Exception as e:
            logger.error(f"Error visualizing monthly spending: {e}")
            raise

    def visualize_category_spending_pie(self, year_month=None):
        """Display category-wise spending as pie chart"""
        try:
            if year_month:
                query = f"""
                SELECT 
                    category,
                    total_amount,
                    transaction_count
                FROM category_wise_spending
                WHERE year_month = '{year_month}'
                ORDER BY total_amount DESC
                """
                title_suffix = f" - {year_month}"
            else:
                query = """
                SELECT 
                    category,
                    SUM(total_amount) as total_amount,
                    SUM(transaction_count) as transaction_count
                FROM category_wise_spending
                GROUP BY category
                ORDER BY total_amount DESC
                """
                title_suffix = " - All Time"
            
            df = pd.read_sql(query, self.engine)
            
            if df.empty:
                logger.warning("No category-wise spending found in database")
                return
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            
            colors = plt.cm.Set3(range(len(df)))
            wedges, texts, autotexts = ax.pie(
                df['total_amount'],
                labels=df['category'],
                autopct='%1.1f%%',
                colors=colors,
                startangle=90
            )
            
            # Enhance text
            for text in texts:
                text.set_fontsize(10)
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            plt.title(f'Category-wise Spending{title_suffix}', fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            plt.savefig('visualizations/category_spending_pie.png', dpi=300, bbox_inches='tight')
            logger.info("Category-wise spending pie chart saved to visualizations/category_spending_pie.png")
            plt.show()
            
        except Exception as e:
            logger.error(f"Error visualizing category spending: {e}")
            raise

    def generate_all_visualizations(self):
        """Generate all visualizations"""
        logger.info("Starting visualization generation...")
        
        # Create visualizations directory if it doesn't exist
        os.makedirs('visualizations', exist_ok=True)
        
        try:
            logger.info("Generating transactions table...")
            self.visualize_transactions_table()
            
            logger.info("Generating monthly spending pie chart...")
            self.visualize_monthly_spending_pie()
            
            logger.info("Generating category-wise spending pie chart...")
            self.visualize_category_spending_pie()
            
            logger.info("All visualizations generated successfully!")
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            raise


if __name__ == "__main__":
    visualizer = FinanceVisualizer()
    visualizer.generate_all_visualizations()
