# Foster Income Survey - Healthcare Product Analysis Platform

## 📋 Project Overview

**Foster Income Survey** is a comprehensive data collection and analysis platform designed to analyze income spending patterns in preparation for a new healthcare product launch. This project combines a Flask web application for data collection, MongoDB Atlas for data storage, and advanced data analysis tools to provide actionable insights for business decision-making.

### 🎯 Project Objectives

1. **Data Collection**: Create a user-friendly web interface to collect participant income and spending data
2. **Data Storage**: Implement secure MongoDB Atlas storage for survey responses
3. **Data Processing**: Develop automated data processing and CSV export capabilities
4. **Data Analysis**: Perform comprehensive analysis to identify target demographics
5. **Visualization**: Generate professional charts and insights for stakeholder presentations
6. **Cloud Deployment**: Host the application on AWS for accessibility and scalability

---

## 🏗️ Project Architecture

```
Foster Income Survey Platform
├── Flask Web Application (AWS Elastic Beanstalk)
├── MongoDB Atlas (Cloud Database)
├── Data Processing Engine (Python Class)
├── Jupyter Analysis Notebook
└── Visualization Exports (PNG Charts)
```

### **Technology Stack**
- **Backend**: Python 3.9, Flask
- **Database**: MongoDB Atlas (Cloud)
- **Cloud Platform**: AWS Elastic Beanstalk
- **Data Analysis**: Pandas, NumPy, Matplotlib, Seaborn
- **Analysis Environment**: Jupyter Notebook
- **Version Control**: Git/GitHub

---

## 📁 Project Structure

```
foster/
├── app.py                          # Main Flask application
├── user_data_processor.py          # User class for data processing
├── Foster_Income_Analysis.ipynb    # Jupyter notebook for analysis
├── requirements.txt                # Python dependencies
├── Procfile                        # Gunicorn configuration for deployment
├── .elasticbeanstalk/             # AWS deployment configuration
├── .ebextensions/                 # EB environment configuration
├── templates/                     # HTML templates
│   └── survey_form.html          # Main survey interface
├── static/                        # Static assets (CSS, JS, images)
├── exports/                       # Generated charts and data files
└── README.md                      # This documentation
```

---

## 🚀 Quick Start Guide

### **Prerequisites**

Before setting up the project, ensure you have:

1. **Python 3.9+** installed
2. **MongoDB Atlas** account (or use provided credentials)
3. **AWS Account** (for deployment)
4. **Git** for version control
5. **Jupyter Notebook** for analysis

### **1. Clone the Repository**

```bash
git clone https://github.com/NeneLartey/DatabyFoster.git
cd DatabyFoster
```

### **2. Environment Setup**

```bash
# Create virtual environment
python -m venv foster_env

# Activate virtual environment
# On Windows:
foster_env\Scripts\activate
# On macOS/Linux:
source foster_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Environment Variables**

Create a `.env` file or set environment variables:

```bash
export MONGO_URI="mongodb+srv://Foster:survey123@cluster0.ypjmsmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
```

### **4. Local Development**

```bash
# Run the Flask application locally
python app.py

# Access the application at:
# http://localhost:5000
```

---

## 🌐 Live Application

**Production URL**: [foster-python-app.eba-uqgvmmsy.us-east-1.elasticbeanstalk.com](http://foster-python-app.eba-uqgvmmsy.us-east-1.elasticbeanstalk.com)

### **Application Features**

1. **Survey Form**: User-friendly interface for data collection
   - Age input validation
   - Gender selection
   - Total income entry
   - Expense categories with checkboxes and amount fields:
     - Utilities
     - Entertainment
     - School Fees
     - Shopping
     - Healthcare

2. **Health Check**: `/health` endpoint for monitoring database connectivity

3. **Data Validation**: Client-side and server-side validation

4. **Responsive Design**: Mobile-friendly interface

---

## 🔧 Data Processing & Analysis

### **User Class (`user_data_processor.py`)**

The `User` class provides comprehensive data processing capabilities:

```python
from user_data_processor import User

# Initialize processor
processor = User()

# Export data to CSV
csv_file = processor.export_to_csv()

# Get summary statistics
stats = processor.get_summary_statistics()

# Close connection
processor.close_connection()
```

#### **Key Features:**
- **Database Connection**: Secure MongoDB Atlas connectivity
- **Data Processing**: Clean and validate survey responses
- **CSV Export**: Automated export with timestamps
- **Statistical Analysis**: Summary statistics generation
- **Error Handling**: Robust error handling and logging

### **Jupyter Analysis (`Foster_Income_Analysis.ipynb`)**

The notebook provides comprehensive analysis including:

1. **Ages with Highest Income**
   - Age group analysis
   - Income distribution by age
   - Statistical summaries

2. **Gender Distribution Across Spending Categories**
   - Gender-based spending patterns
   - Category-wise analysis
   - Percentage of income allocation

3. **Healthcare Spending Analysis**
   - Healthcare spending patterns
   - Target demographic identification
   - Product launch recommendations

#### **Generated Outputs:**
- `ages_highest_income_analysis.png`
- `gender_distribution_spending_categories.png`
- `healthcare_spending_analysis.png`
- `foster_analysis_data.csv`
- `demographic_summary.csv`
- `high_value_targets.csv`

---

## 📊 Running the Analysis

### **Step 1: Data Collection**
1. Access the web application
2. Fill out survey forms
3. Data is automatically stored in MongoDB Atlas

### **Step 2: Data Processing**
```bash
# Run the User class to export data
python user_data_processor.py
```

### **Step 3: Analysis**
```bash
# Start Jupyter Notebook
jupyter notebook Foster_Income_Analysis.ipynb

# Run all cells to generate analysis and charts
```

### **Step 4: Results**
- Charts exported as PNG files for PowerPoint presentations
- CSV files generated for further analysis
- Statistical summaries displayed in notebook

---

## ☁️ AWS Deployment

### **Current Deployment**
- **Platform**: AWS Elastic Beanstalk
- **Environment**: Python 3.9
- **Region**: us-east-1
- **Instance Type**: Single instance (cost-optimized)

### **Deployment Commands**
```bash
# Initialize EB CLI (if not already done)
eb init

# Deploy to production
eb deploy

# Check application health
eb health

# View logs
eb logs
```

### **Environment Variables (AWS)**
The application uses the following environment variables:
- `MONGO_URI`: MongoDB Atlas connection string

---

## 🔐 Database Configuration

### **MongoDB Atlas Setup**

**Connection Details:**
- **Cluster**: cluster0.ypjmsmr.mongodb.net
- **Database**: Foster
- **Collection**: user_data
- **Username**: Foster
- **Password**: survey123

**Security Features:**
- IP Whitelisting: Configured for AWS access
- TLS/SSL: Enabled with certificate validation
- Authentication: Username/password protection

### **Data Schema**
```json
{
  "_id": "ObjectId",
  "age": "Integer",
  "gender": "String",
  "total_income": "Float",
  "expenses": {
    "utilities": "Float",
    "entertainment": "Float",
    "school_fees": "Float",
    "shopping": "Float",
    "healthcare": "Float"
  },
  "submission_time": "DateTime"
}
```

---

## 📈 Analysis Results

### **Key Findings**

1. **Target Demographics**
   - Highest income age groups identified
   - Gender-based spending patterns analyzed
   - Healthcare spending priorities established

2. **Business Insights**
   - Market segmentation recommendations
   - Pricing strategy guidance
   - Target audience prioritization

3. **Product Launch Strategy**
   - High-value customer segments identified
   - Marketing approach recommendations
   - Revenue opportunity assessment

---

## 🔍 Monitoring & Health Checks

### **Application Health**
- **Endpoint**: `/health`
- **Database Connectivity**: Real-time MongoDB connection status
- **Response Format**: JSON with status indicators

### **Logging**
- Application logs available via `eb logs`
- Error tracking and debugging support
- Performance monitoring

---

## 🛠️ Troubleshooting

### **Common Issues**

1. **MongoDB Connection Issues**
   ```bash
   # Check environment variables
   echo $MONGO_URI
   
   # Test connection locally
   python -c "from pymongo import MongoClient; client = MongoClient('your_uri'); client.admin.command('ping'); print('Connected!')"
   ```

2. **AWS Deployment Issues**
   ```bash
   # Check EB status
   eb status
   
   # View detailed logs
   eb logs --all
   
   # Restart application
   eb deploy --force
   ```

3. **Jupyter Notebook Issues**
   ```bash
   # Install Jupyter if missing
   pip install jupyter
   
   # Start notebook server
   jupyter notebook --ip=0.0.0.0 --port=8888
   ```

### **Error Resolution**

**SSL/TLS Connection Errors:**
- Verify MongoDB Atlas IP whitelist
- Check TLS configuration in connection string
- Ensure certificate validation settings

**Data Processing Errors:**
- Validate data types in survey responses
- Check for missing required fields
- Review data cleaning logic

---

## 📝 Development Guidelines

### **Code Standards**
- **PEP 8**: Python code style compliance
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust exception handling
- **Logging**: Informative logging throughout application

### **Testing**
```bash
# Test database connection
python user_data_processor.py

# Test web application locally
python app.py

# Test health endpoint
curl http://localhost:5000/health
```

### **Git Workflow**
```bash
# Standard development workflow
git add .
git commit -m "Feature: Description of changes"
git push origin main

# Deploy changes
eb deploy --staged
```

---

## 📚 Dependencies

### **Core Dependencies**
```
flask==2.3.3
pymongo[srv]==4.5.0
pandas==2.1.1
matplotlib==3.7.2
seaborn==0.12.2
jupyter==1.0.0
gunicorn==21.2.0
```

### **Development Dependencies**
```
python-dotenv==1.0.0
certifi==2023.7.22
```

---

## 👥 Contributors

- **Foster Data Team**
- **Lead Developer**: Data Analysis Specialist
- **Project Manager**: Healthcare Product Team
- **Stakeholders**: Foster Healthcare Division

---

## 📄 License

This project is proprietary software developed for Foster Healthcare product analysis. Unauthorized reproduction or distribution is prohibited.

---

## 📞 Support

For technical support or questions about this project:

1. **Check Documentation**: Review this README and code comments
2. **Review Logs**: Check application logs for error details
3. **Test Connectivity**: Verify database and AWS connections
4. **Contact Team**: Reach out to the Foster Data Team

---

## 🔄 Version History

- **v1.0** (May 2025): Initial release with full functionality
  - Flask web application deployed to AWS
  - MongoDB Atlas integration
  - User class for data processing
  - Jupyter notebook analysis
  - Comprehensive documentation

---

## 🎯 Next Steps

1. **Data Collection**: Gather more survey responses
2. **Advanced Analytics**: Implement machine learning models
3. **Dashboard**: Create real-time analytics dashboard
4. **API Integration**: Develop RESTful API for data access
5. **Mobile App**: Consider mobile application development

---

**© 2025 Foster Healthcare - Income Survey Analysis Platform** 