import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from ETL.transactionDataManager import TransactionDataManager
from TAS.analyseTransactions import TransactionAnalyser
from config import DATABASE_URI
from basic_visualizer import FinanceVisualizer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_etl_pipeline():
    """
    Run the ETL pipeline to load and transform transaction data
    """
    logger.info("=" * 60)
    logger.info("STARTING ETL PIPELINE")
    logger.info("=" * 60)
    
    # print("Select the data file to load: \n1. Sample Data \n2.Personal Data")
    
    try:
        manager = TransactionDataManager()
        file_path = 'DATA/sampleData.csv'
        manager.process_and_store(file_path)
        logger.info("ETL Pipeline completed successfully")
        return True
    except Exception as e:
        logger.error(f"ETL Pipeline failed: {e}")
        return False


def run_transaction_analysis():
    """
    Run the Transaction Analysis to generate spending summaries
    """
    logger.info("=" * 60)
    logger.info("STARTING TRANSACTION ANALYSIS")
    logger.info("=" * 60)
    
    try:
        analyser = TransactionAnalyser(db_uri=DATABASE_URI)
        
        # Calculate monthly spending summary
        logger.info("Calculating monthly spending summary...")
        monthly_summary = analyser.calculate_monthly_spending_summary()
        logger.info(f"Monthly spending summary generated for {len(monthly_summary)} months")
        print("\n--- Monthly Spending Summary ---")
        print(monthly_summary.to_string())
        
        # Calculate category-wise spending
        logger.info("Calculating category-wise spending...")
        category_summary = analyser.calculate_category_wise_spending()
        logger.info(f"Category-wise spending generated for {len(category_summary)} category-month combinations")
        print("\n--- Category-wise Spending ---")
        print(category_summary.to_string())
        
        analyser.close()
        logger.info("Transaction Analysis completed successfully")
        return True
    except Exception as e:
        logger.error(f"Transaction Analysis failed: {e}")
        return False


def main():
    """
    Main driver function to orchestrate ETL and Analysis
    """
    logger.info("PERSONAL FINANCE ANALYTICS - FULL PIPELINE")
    logger.info("Starting ETL and Analysis workflow...")
    
    # Run ETL Pipeline
    etl_success = run_etl_pipeline()
    
    if not etl_success:
        logger.error("ETL Pipeline failed. Aborting analysis.")
        return
    
    # Run Transaction Analysis
    analysis_success = run_transaction_analysis()
    
    if analysis_success:
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
    else:
        logger.error("Pipeline completed with errors")
        return
    
    # Generate Visualizations
    logger.info("Generating visualizations...")
    try:
        visualizer = FinanceVisualizer(db_uri=DATABASE_URI)
        visualizer.generate_all_visualizations()
        logger.info("Visualizations generated successfully")
    except Exception as e:
        logger.error(f"Visualization generation failed: {e}")   


if __name__ == "__main__":
    main()