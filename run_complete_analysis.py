#!/usr/bin/env python3
"""
Foster Income Survey - Complete Analysis Workflow
================================================

This script demonstrates the complete workflow of the Foster Income Survey project,
from data processing to analysis and visualization generation.

Usage:
    python run_complete_analysis.py

Author: Foster Data Team
Date: May 2025
"""

import os
import sys
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis_workflow.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Execute the complete Foster Income Survey analysis workflow
    """
    print("🚀 Foster Income Survey - Complete Analysis Workflow")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Step 1: Import and test User data processor
        print("📥 Step 1: Initializing User Data Processor...")
        from user_data_processor import User
        
        user_processor = User()
        logger.info("✅ User data processor initialized successfully")
        
        # Step 2: Get summary statistics
        print("\n📊 Step 2: Generating Summary Statistics...")
        stats = user_processor.get_summary_statistics()
        
        if stats:
            print(f"   - Total Respondents: {stats['total_respondents']}")
            print(f"   - Average Income: ${stats['average_income']:,.2f}")
            print(f"   - Average Age: {stats['average_age']:.1f} years")
            print(f"   - Gender Distribution: {stats['gender_distribution']}")
            print(f"   - Average Healthcare Spending: ${stats['expense_categories_avg']['healthcare']:,.2f}")
            logger.info("✅ Summary statistics generated successfully")
        else:
            print("   ⚠️ No data found in database")
            logger.warning("No data found for analysis")
        
        # Step 3: Export data to CSV
        print("\n💾 Step 3: Exporting Data to CSV...")
        csv_filename = user_processor.export_to_csv(filename="complete_analysis_export.csv")
        
        if csv_filename:
            print(f"   ✅ Data exported to: {csv_filename}")
            logger.info(f"Data exported to {csv_filename}")
        else:
            print("   ❌ Failed to export data")
            logger.error("Failed to export data to CSV")
        
        # Step 4: Close database connection
        user_processor.close_connection()
        logger.info("Database connection closed")
        
        # Step 5: Check if Jupyter notebook exists
        print("\n📓 Step 4: Checking Analysis Components...")
        
        notebook_file = "Foster_Income_Analysis.ipynb"
        if os.path.exists(notebook_file):
            print(f"   ✅ Jupyter notebook found: {notebook_file}")
            print("   📋 To run analysis:")
            print(f"      jupyter notebook {notebook_file}")
            logger.info("Jupyter notebook is available for analysis")
        else:
            print(f"   ❌ Jupyter notebook not found: {notebook_file}")
            logger.error("Jupyter notebook is missing")
        
        # Step 6: Check web application
        print("\n🌐 Step 5: Web Application Status...")
        print("   🔗 Production URL: http://foster-python-app.eba-uqgvmmsy.us-east-1.elasticbeanstalk.com")
        print("   🏥 Health Check: http://foster-python-app.eba-uqgvmmsy.us-east-1.elasticbeanstalk.com/health")
        
        # Step 7: List generated files
        print("\n📁 Step 6: Generated Files...")
        files_to_check = [
            "complete_analysis_export.csv",
            "foster_analysis_data.csv", 
            "user_data_processor.py",
            "Foster_Income_Analysis.ipynb",
            "README.md"
        ]
        
        for file in files_to_check:
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                print(f"   ✅ {file} ({file_size:,} bytes)")
            else:
                print(f"   ❌ {file} (missing)")
        
        # Step 8: Display next steps
        print("\n🎯 Next Steps:")
        print("=" * 15)
        print("1. 📊 Run Jupyter Analysis:")
        print("   jupyter notebook Foster_Income_Analysis.ipynb")
        print()
        print("2. 🌐 Collect More Data:")
        print("   Visit: http://foster-python-app.eba-uqgvmmsy.us-east-1.elasticbeanstalk.com")
        print()
        print("3. 📈 Generate Charts:")
        print("   Run all cells in the Jupyter notebook to create:")
        print("   - ages_highest_income_analysis.png")
        print("   - gender_distribution_spending_categories.png")
        print("   - healthcare_spending_analysis.png")
        print()
        print("4. 💼 PowerPoint Integration:")
        print("   Use the generated PNG files in your presentation")
        print()
        print("5. 🔄 Continuous Analysis:")
        print("   Re-run this script after collecting more survey data")
        
        print(f"\n✅ Complete analysis workflow finished successfully!")
        print(f"   Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("Complete analysis workflow finished successfully")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Please ensure all required packages are installed:")
        print("   pip install -r requirements.txt")
        logger.error(f"Import error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        logger.error(f"Unexpected error: {e}")
        raise

def check_requirements():
    """
    Check if all required packages are installed
    """
    required_packages = [
        'flask', 'pymongo', 'pandas', 'matplotlib', 
        'seaborn', 'jupyter', 'gunicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("⚠️ Missing Required Packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def display_project_info():
    """
    Display project information and structure
    """
    print("📁 Foster Income Survey Project Structure:")
    print("=" * 45)
    
    structure = {
        "app.py": "Flask web application (deployed to AWS)",
        "user_data_processor.py": "User class for data processing and CSV export",
        "Foster_Income_Analysis.ipynb": "Jupyter notebook for analysis and visualization",
        "requirements.txt": "Python package dependencies",
        "README.md": "Comprehensive project documentation",
        "Procfile": "Gunicorn configuration for AWS deployment",
        "templates/": "HTML templates for web interface",
        "static/": "CSS and static assets",
        ".elasticbeanstalk/": "AWS Elastic Beanstalk configuration"
    }
    
    for item, description in structure.items():
        status = "✅" if os.path.exists(item) else "❌"
        print(f"{status} {item:<30} - {description}")

if __name__ == "__main__":
    # Display project info
    display_project_info()
    print()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Run main workflow
    main() 