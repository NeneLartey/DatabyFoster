from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configure MongoDB
# Use MONGO_URI from environment variable if available, otherwise default to localhost
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/survey_db') # Default includes db name
client = MongoClient(mongo_uri)

# Try to get DB name from URI path, otherwise use 'survey_db' as a fallback
db_name = 'survey_db' # Default database name
try:
    path_part = mongo_uri.split('/', 3)[-1] # Get the part after mongodb://host:port/
    if path_part and '?' in path_part: # Handle query parameters
        db_name_candidate = path_part.split('?')[0]
        if db_name_candidate: # ensure it's not an empty string if URI ends with /?
            db_name = db_name_candidate
    elif path_part: # No query parameters
        db_name_candidate = path_part
        if db_name_candidate: # ensure it's not an empty string if URI ends with /
            db_name = db_name_candidate
except IndexError:
    # This might happen if the URI format is unexpected, stick to default
    pass 

db = client[db_name] 
survey_collection = db['user_data'] # Collection name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process form data
        user_data = {
            "age": request.form.get('age'),
            "gender": request.form.get('gender'),
            "total_income": request.form.get('total_income'),
            "expenses": {
                "utilities": request.form.get('utilities_amount'),
                "entertainment": request.form.get('entertainment_amount'),
                "school_fees": request.form.get('school_fees_amount'),
                "shopping": request.form.get('shopping_amount'),
                "healthcare": request.form.get('healthcare_amount')
            }
        }
        
        # Store data in MongoDB
        survey_collection.insert_one(user_data)
        
        return redirect(url_for('thank_you')) # Or redirect to a thank you page

    return render_template('index.html')

@app.route('/thank-you')
def thank_you():
    return "Thank you for participating in the survey!"

if __name__ == '__main__':
    app.run(debug=True) 