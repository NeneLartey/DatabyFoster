import pandas as pd
from pymongo import MongoClient
import os

class User:
    def __init__(self, mongo_uri=None, db_name='survey_db', collection_name='user_data'):
        """
        Initializes the User class with MongoDB connection details.
        If mongo_uri is not provided, it attempts to get it from the MONGO_URI environment variable.
        If still not found, defaults to 'mongodb://localhost:27017/'.
        The db_name can be part of the mongo_uri or specified separately.

        Args:
            mongo_uri (str, optional): The MongoDB connection string (e.g., 'mongodb://host:port/dbname').
            db_name (str): The name of the database. Ignored if dbname is in mongo_uri.
            collection_name (str): The name of the collection.
        """
        if mongo_uri is None:
            mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/survey_db')

        self.client = MongoClient(mongo_uri)
        
        # Try to get DB name from URI, otherwise use provided db_name or default from URI parsing
        try:
            parsed_db_name = mongo_uri.split('/')[-1].split('?')[0] # Get path part, remove query params
            if parsed_db_name:
                self.db = self.client[parsed_db_name]
            else:
                self.db = self.client[db_name]
        except Exception:
             self.db = self.client[db_name] # Fallback

        self.collection = self.db[collection_name]

    def fetch_data(self):
        """
        Fetches all data from the specified MongoDB collection.

        Returns:
            list: A list of documents (dictionaries) from the collection.
        """
        data = list(self.collection.find())
        return data

    def _preprocess_data(self, survey_data):
        """
        Preprocesses the raw data fetched from MongoDB to flatten the expenses 
        and handle potential missing values for amounts if a category was not selected.

        Args:
            survey_data (list): A list of survey documents from MongoDB.

        Returns:
            list: A list of preprocessed dictionaries, ready for DataFrame conversion.
        """
        processed_data = []
        for record in survey_data:
            flat_record = {
                'age': record.get('age'),
                'gender': record.get('gender'),
                'total_income': record.get('total_income')
            }
            expenses = record.get('expenses', {})
            flat_record['utilities_expense'] = expenses.get('utilities')
            flat_record['entertainment_expense'] = expenses.get('entertainment')
            flat_record['school_fees_expense'] = expenses.get('school_fees')
            flat_record['shopping_expense'] = expenses.get('shopping')
            flat_record['healthcare_expense'] = expenses.get('healthcare')
            processed_data.append(flat_record)
        return processed_data

    def store_data_as_csv(self, file_path='survey_data.csv'):
        """
        Fetches data from MongoDB, preprocesses it, and stores it in a CSV file.

        Args:
            file_path (str): The path to the CSV file where data will be stored.
        """
        survey_data = self.fetch_data()
        if not survey_data:
            print("No data found in MongoDB collection.")
            return

        preprocessed_survey_data = self._preprocess_data(survey_data)
        
        df = pd.DataFrame(preprocessed_survey_data)

        # Convert relevant columns to numeric, coercing errors to NaN
        numeric_cols = ['age', 'total_income', 'utilities_expense', 'entertainment_expense', 
                        'school_fees_expense', 'shopping_expense', 'healthcare_expense']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.to_csv(file_path, index=False)
        print(f"Data successfully stored in {file_path}")

if __name__ == '__main__':
    # Example usage:
    user_processor = User()
    # Ensure you have some data in MongoDB before running this
    # You can run the Flask app (app.py) and submit some survey responses.
    user_processor.store_data_as_csv() 