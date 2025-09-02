# 🎓 EdTech Analytics Project

Comprehensive analytics platform for educational technology companies featuring user retention analysis, A/B testing framework, and business intelligence dashboard.

## 📊 Key Features

- **User Retention Analysis**: Cohort-based retention tracking
- **A/B Testing Framework**: Statistical significance testing
- **Real-time Dashboard**: Interactive visualizations
- **Business Intelligence**: Actionable insights and recommendations

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/edtech-analytics-project.git
cd edtech-analytics-project

# Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database
cp .env.example .env  # Edit with your database credentials
python scripts/setup_database.py
python scripts/generate_sample_data.py

# Launch dashboard
python dashboard/app.py
# Open http://localhost:8050 in your browser
