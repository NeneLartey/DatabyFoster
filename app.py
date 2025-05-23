from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
import ssl

# Elastic Beanstalk expects 'application' variable name
application = Flask(__name__)

# Configure MongoDB with proper error handling and AWS-compatible SSL fix
# Updated with corrected TLS parameters - deployment v2
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/survey_db')

try:
    # Try multiple connection approaches for maximum AWS compatibility
    connection_options = [
        # Option 1: PyMongo-compatible SSL parameters (fixed conflicting options)
        {
            'serverSelectionTimeoutMS': 5000,
            'connectTimeoutMS': 5000,
            'socketTimeoutMS': 5000,
            'tls': True,
            'tlsAllowInvalidCertificates': True,
            'tlsAllowInvalidHostnames': True
        },
        # Option 2: Standard connection without explicit SSL config
        {
            'serverSelectionTimeoutMS': 10000,
            'connectTimeoutMS': 10000,
            'socketTimeoutMS': 10000
        },
        # Option 3: Connection with minimal TLS
        {
            'serverSelectionTimeoutMS': 15000,
            'tls': False if 'localhost' in mongo_uri else True,
            'directConnection': False
        }
    ]
    
    client = None
    for i, options in enumerate(connection_options):
        try:
            print(f"🔄 Attempting MongoDB connection method {i+1} with options: {list(options.keys())}")
            client = MongoClient(mongo_uri, **options)
            # Test the connection
            client.admin.command('ping')
            print(f"✅ Successfully connected to MongoDB using method {i+1}!")
            break
        except Exception as e:
            print(f"❌ Connection method {i+1} failed: {e}")
            if client:
                client.close()
                client = None
            continue
    
    if client is None:
        raise Exception("All connection methods failed")
    
    # Extract database name from URI or use default
    db_name = 'Foster'  # Default database name
    try:
        if '/' in mongo_uri and '?' in mongo_uri:
            # Extract database name from URI if present
            path_part = mongo_uri.split('/')[-1].split('?')[0]
            if path_part and path_part != '':
                db_name = path_part
    except:
        pass
    
    db = client[db_name]
    survey_collection = db['user_data']
    print(f"📊 Using database: {db_name}")
    
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    # For development/testing, you might want to handle this differently
    db = None
    survey_collection = None

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if survey_collection is None:
            return "Database connection error. Please check MongoDB configuration.", 500
            
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
        
        try:
            # Store data in MongoDB
            result = survey_collection.insert_one(user_data)
            print(f"✅ Data saved with ID: {result.inserted_id}")
            return redirect(url_for('thank_you'))
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return "Error saving data to database.", 500

    return render_template('index.html')

@application.route('/thank-you')
def thank_you():
    return "Thank you for participating in the Foster Income Survey!"

@application.route('/health')
def health_check():
    """Health check endpoint for deployment verification"""
    try:
        if survey_collection is not None:
            # Test database connection
            survey_collection.find_one()
            return {"status": "healthy", "database": "connected"}, 200
        else:
            return {"status": "unhealthy", "database": "disconnected"}, 500
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

if __name__ == '__main__':
    application.run(debug=True) 