"""
Foster Income Survey - User Data Processor
==========================================

This module contains the User class for processing survey data collected from the Flask application.
The class handles data retrieval from MongoDB and exports data to CSV format for analysis.

Author: Foster Data Team
Date: May 2025
Purpose: Income spending analysis for healthcare product launch
"""

import pandas as pd
import pymongo
from pymongo import MongoClient
import os
from datetime import datetime
import logging

# Configure logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class User:
    """
    User Data Processor Class
    
    This class handles the processing of user survey data from MongoDB Atlas.
    It provides functionality to:
    - Connect to MongoDB database
    - Retrieve all user survey responses
    - Process and clean the data
    - Export data to CSV format for analysis
    - Generate summary statistics
    
    Attributes:
        mongo_uri (str): MongoDB connection string
        db_name (str): Database name in MongoDB
        collection_name (str): Collection name for user data
        client (MongoClient): MongoDB client connection
        db: Database object
        collection: Collection object for user data
    """
    
    def __init__(self, mongo_uri=None, db_name="Foster", collection_name="user_data"):
        """
        Initialize the User data processor
        
        Args:
            mongo_uri (str): MongoDB connection string. If None, uses environment variable
            db_name (str): Name of the database (default: "Foster")
            collection_name (str): Name of the collection (default: "user_data")
        """
        # Set up MongoDB connection parameters
        self.mongo_uri = mongo_uri or os.environ.get('MONGO_URI', 
            'mongodb+srv://Foster:survey123@cluster0.ypjmsmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.db_name = db_name
        self.collection_name = collection_name
        
        # Initialize connection objects
        self.client = None
        self.db = None
        self.collection = None
        
        # Connect to MongoDB
        self._connect_to_database()
        
        logger.info(f"User data processor initialized for database: {db_name}")
    
    def _connect_to_database(self):
        """
        Establish connection to MongoDB Atlas
        
        This method creates a connection to MongoDB using the provided URI,
        sets up the database and collection references, and tests the connection.
        
        Raises:
            Exception: If connection to MongoDB fails
        """
        try:
            # Create MongoDB client with optimized connection settings
            self.client = MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=10000,  # 10 second timeout
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                tls=True,
                tlsAllowInvalidCertificates=True,
                tlsAllowInvalidHostnames=True
            )
            
            # Test the connection
            self.client.admin.command('ping')
            logger.info("✅ Successfully connected to MongoDB Atlas")
            
            # Set up database and collection references
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            
            # Verify collection access
            collection_count = self.collection.estimated_document_count()
            logger.info(f"📊 Connected to collection '{self.collection_name}' with {collection_count} documents")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise Exception(f"Database connection failed: {e}")
    
    def get_all_user_data(self):
        """
        Retrieve all user survey data from MongoDB
        
        Returns:
            list: List of dictionaries containing all user survey responses
        """
        try:
            # Retrieve all documents from the collection
            cursor = self.collection.find({})
            user_data_list = list(cursor)
            
            logger.info(f"📥 Retrieved {len(user_data_list)} user survey responses")
            return user_data_list
            
        except Exception as e:
            logger.error(f"❌ Error retrieving user data: {e}")
            return []
    
    def process_user_data(self):
        """
        Process and clean user data from MongoDB
        
        This method retrieves raw data from MongoDB, processes it into a clean format,
        and structures it for analysis and CSV export.
        
        Returns:
            pandas.DataFrame: Processed user data in tabular format
        """
        # Get raw data from MongoDB
        raw_data = self.get_all_user_data()
        
        if not raw_data:
            logger.warning("⚠️ No user data found in database")
            return pd.DataFrame()
        
        # Process each user record
        processed_records = []
        
        for record in raw_data:
            try:
                # Extract basic user information
                processed_record = {
                    'user_id': str(record.get('_id', '')),
                    'age': record.get('age', None),
                    'gender': record.get('gender', ''),
                    'total_income': float(record.get('total_income', 0)) if record.get('total_income') else 0,
                    'submission_time': record.get('_id').generation_time if record.get('_id') else datetime.now()
                }
                
                # Extract expense data
                expenses = record.get('expenses', {})
                processed_record.update({
                    'utilities_expense': float(expenses.get('utilities', 0)) if expenses.get('utilities') else 0,
                    'entertainment_expense': float(expenses.get('entertainment', 0)) if expenses.get('entertainment') else 0,
                    'school_fees_expense': float(expenses.get('school_fees', 0)) if expenses.get('school_fees') else 0,
                    'shopping_expense': float(expenses.get('shopping', 0)) if expenses.get('shopping') else 0,
                    'healthcare_expense': float(expenses.get('healthcare', 0)) if expenses.get('healthcare') else 0
                })
                
                # Calculate total expenses
                total_expenses = sum([
                    processed_record['utilities_expense'],
                    processed_record['entertainment_expense'], 
                    processed_record['school_fees_expense'],
                    processed_record['shopping_expense'],
                    processed_record['healthcare_expense']
                ])
                processed_record['total_expenses'] = total_expenses
                
                # Calculate savings (income - expenses)
                processed_record['savings'] = processed_record['total_income'] - total_expenses
                
                # Calculate expense percentages of total income
                if processed_record['total_income'] > 0:
                    processed_record['utilities_percentage'] = (processed_record['utilities_expense'] / processed_record['total_income']) * 100
                    processed_record['entertainment_percentage'] = (processed_record['entertainment_expense'] / processed_record['total_income']) * 100
                    processed_record['school_fees_percentage'] = (processed_record['school_fees_expense'] / processed_record['total_income']) * 100
                    processed_record['shopping_percentage'] = (processed_record['shopping_expense'] / processed_record['total_income']) * 100
                    processed_record['healthcare_percentage'] = (processed_record['healthcare_expense'] / processed_record['total_income']) * 100
                    processed_record['total_expenses_percentage'] = (total_expenses / processed_record['total_income']) * 100
                else:
                    # Handle zero income cases
                    processed_record.update({
                        'utilities_percentage': 0, 'entertainment_percentage': 0,
                        'school_fees_percentage': 0, 'shopping_percentage': 0,
                        'healthcare_percentage': 0, 'total_expenses_percentage': 0
                    })
                
                processed_records.append(processed_record)
                
            except Exception as e:
                logger.warning(f"⚠️ Error processing record {record.get('_id', 'unknown')}: {e}")
                continue
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(processed_records)
        
        if not df.empty:
            # Data type conversions and validations
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            df['total_income'] = pd.to_numeric(df['total_income'], errors='coerce')
            
            # Remove records with invalid ages or incomes
            df = df.dropna(subset=['age', 'total_income'])
            
            logger.info(f"✅ Successfully processed {len(df)} valid user records")
        else:
            logger.warning("⚠️ No valid records after processing")
        
        return df
    
    def export_to_csv(self, filename=None, include_timestamp=True):
        """
        Export processed user data to CSV file
        
        Args:
            filename (str): Output filename. If None, auto-generates with timestamp
            include_timestamp (bool): Whether to include timestamp in filename
            
        Returns:
            str: Path to the exported CSV file
        """
        # Process the data
        df = self.process_user_data()
        
        if df.empty:
            logger.error("❌ No data to export")
            return None
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if include_timestamp else ""
            filename = f"foster_survey_data_{timestamp}.csv" if timestamp else "foster_survey_data.csv"
        
        try:
            # Export to CSV
            df.to_csv(filename, index=False)
            logger.info(f"✅ Successfully exported {len(df)} records to {filename}")
            
            # Display summary statistics
            self._display_export_summary(df, filename)
            
            return filename
            
        except Exception as e:
            logger.error(f"❌ Error exporting to CSV: {e}")
            return None
    
    def _display_export_summary(self, df, filename):
        """
        Display summary information about the exported data
        
        Args:
            df (pandas.DataFrame): The exported DataFrame
            filename (str): Name of the exported file
        """
        print(f"\n📊 Export Summary for {filename}")
        print("=" * 50)
        print(f"Total Records: {len(df)}")
        print(f"Date Range: {df['submission_time'].min()} to {df['submission_time'].max()}")
        print(f"Age Range: {df['age'].min():.0f} - {df['age'].max():.0f} years")
        print(f"Income Range: ${df['total_income'].min():.2f} - ${df['total_income'].max():.2f}")
        print(f"Average Income: ${df['total_income'].mean():.2f}")
        print(f"Gender Distribution:")
        for gender, count in df['gender'].value_counts().items():
            print(f"  - {gender}: {count} ({count/len(df)*100:.1f}%)")
        print("=" * 50)
    
    def get_summary_statistics(self):
        """
        Generate summary statistics for the user data
        
        Returns:
            dict: Dictionary containing various summary statistics
        """
        df = self.process_user_data()
        
        if df.empty:
            return {}
        
        # Calculate comprehensive statistics
        stats = {
            'total_respondents': len(df),
            'average_age': df['age'].mean(),
            'age_range': {'min': df['age'].min(), 'max': df['age'].max()},
            'average_income': df['total_income'].mean(),
            'income_range': {'min': df['total_income'].min(), 'max': df['total_income'].max()},
            'gender_distribution': df['gender'].value_counts().to_dict(),
            'average_total_expenses': df['total_expenses'].mean(),
            'average_savings': df['savings'].mean(),
            'expense_categories_avg': {
                'utilities': df['utilities_expense'].mean(),
                'entertainment': df['entertainment_expense'].mean(),
                'school_fees': df['school_fees_expense'].mean(),
                'shopping': df['shopping_expense'].mean(),
                'healthcare': df['healthcare_expense'].mean()
            }
        }
        
        return stats
    
    def close_connection(self):
        """
        Close the MongoDB connection
        """
        if self.client:
            self.client.close()
            logger.info("🔒 MongoDB connection closed")


# Example usage and testing
if __name__ == "__main__":
    print("🚀 Foster Income Survey - User Data Processor")
    print("=" * 50)
    
    try:
        # Initialize the User data processor
        user_processor = User()
        
        # Get summary statistics
        stats = user_processor.get_summary_statistics()
        if stats:
            print(f"📊 Found {stats['total_respondents']} survey responses")
            print(f"💰 Average Income: ${stats['average_income']:.2f}")
            print(f"👥 Gender Distribution: {stats['gender_distribution']}")
        
        # Export data to CSV
        csv_file = user_processor.export_to_csv()
        if csv_file:
            print(f"✅ Data exported successfully to: {csv_file}")
        
        # Close connection
        user_processor.close_connection()
        
    except Exception as e:
        print(f"❌ Error: {e}") 