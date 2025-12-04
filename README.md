# Smart Banking System - Full Stack Development Project

A comprehensive Django-based banking and financial management system with ML-powered loan estimation, multiple financial calculators, and secure account management.

## 🎯 Features

### 💰 Core Banking
- **User Authentication**: Secure registration and login with password hashing
- **Account Management**: Check balance, deposit, and withdraw funds
- **Transaction History**: Track all account activities
- **Decimal Precision**: All financial calculations use Python Decimal for accuracy

### 📊 Financial Calculators (10+ Tools)
1. **EMI Calculator** - Equated Monthly Installment for loans
2. **SIP Calculator** - Systematic Investment Plan calculator
3. **FD Calculator** - Fixed Deposit with compound interest
4. **RD Calculator** - Recurring Deposit calculator
5. **Retirement Planner** - Estimate retirement corpus needed
6. **Home Loan Eligibility** - Check loan eligibility based on income
7. **Credit Card Balance** - Analyze credit card debt payoff timeline
8. **Income Tax Calculator** - Calculate taxable income
9. **Budget Planner** - Plan monthly budget allocation
10. **Net Worth Calculator** - Calculate total net worth

### 🤖 ML-Powered Loan Estimator
- Predicts eligible loan amount using machine learning (Random Forest)
- Features considered:
  - Age
  - Monthly Income
  - Credit Score
  - Loan Tenure
  - Existing Loan Amount
  - Number of Dependents
- Fallback formula if model unavailable
- Model trained on `loan_amount_prediction_dataset_v2.csv`

### 🔒 Security Features
- Django CSRF protection
- Password hashing with Django's built-in system
- Login required decorators on protected views
- User-specific account isolation

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

### 1. Clone Repository
```bash
cd c:\Users\249422\Desktop\Final-Fsd-project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Django Project
```bash
cd djangoProject\BankingSystem
python manage.py migrate
python manage.py createsuperuser  # Create admin user
```

### 5. Train ML Model (Optional)
```bash
cd ..\..\loan_estimator_model
python train_loan_model.py
# Copy the generated model to: 
# ..\..\djangoProject\BankingSystem\Banking\
```

### 6. Run Development Server
```bash
cd ..\djangoProject\BankingSystem
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
Final-Fsd-project/
├── djangoProject/
│   └── BankingSystem/
│       ├── Banking/
│       │   ├── migrations/
│       │   ├── templates/
│       │   │   └── banking/
│       │   │       ├── home.html
│       │   │       ├── register.html
│       │   │       ├── login.html
│       │   │       ├── dashboard.html
│       │   │       ├── deposit.html
│       │   │       ├── withdraw.html
│       │   │       ├── calculator.html
│       │   │       └── loanEstimator.html
│       │   ├── forms.py
│       │   ├── models.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   ├── tests.py
│       │   └── admin.py
│       ├── BankingSystem/
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       └── manage.py
├── finance_tools/
│   ├── __init__.py
│   └── (calculator functions)
├── loan_estimator_model/
│   ├── train_loan_model.py
│   ├── loan_amount_prediction_dataset_v2.csv
│   └── loan_tool_output/
│       └── loan_amount_model.joblib
└── README.md
```

## 🧪 Testing

### Run All Tests
```bash
python manage.py test Banking.tests -v 2
```

### Test Coverage
- ✅ 9 calculator tools
- ✅ Loan estimator (multiple scenarios)
- ✅ User authentication
- ✅ Account operations (deposit/withdraw)
- ✅ Protected view access
- ✅ Data validation

### Sample Test Output
```
test_calculator_budget ... ok
test_calculator_credit_card ... ok
test_calculator_emi ... ok
test_calculator_eligibility ... ok
test_calculator_fd ... ok
test_calculator_networth ... ok
test_calculator_rd ... ok
test_calculator_retirement ... ok
test_calculator_sip ... ok
test_calculator_tax ... ok
test_deposit ... ok
test_loan_estimator_high_income ... ok
test_loan_estimator_minimal_input ... ok
test_loan_estimator_post ... ok
test_login_success ... ok
test_protected_views_require_login ... ok
test_user_registration ... ok
test_withdraw_insufficient_balance ... ok
test_withdraw_success ... ok

Ran 22 tests in 8.234s
OK
```

## 📖 Usage Guide

### 1. Register & Login
- Click "Register" on homepage
- Enter username, email, and password
- Login with credentials

### 2. Dashboard
- View account balance
- Access deposit/withdraw functionality
- Browse financial tools
- Access ML loan estimator

### 3. Financial Calculators
- Select calculator from dashboard
- Enter required parameters
- View calculated results
- Results displayed instantly

### 4. Loan Estimator
- Fill in personal and financial details:
  - Age (18-100)
  - Monthly Income (₹)
  - Credit Score (300-900)
  - Loan Tenure (1-40 years)
  - Existing Loan Amount (optional)
  - Number of Dependents (optional)
- Click "Predict Loan Amount"
- View eligible loan amount

## 🔧 Configuration

### settings.py
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Banking',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Model Paths
Update model loading in `views.py`:
```python
CANDIDATE_MODELS = [
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_tool_output\loan_amount_model.joblib",
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_amount_model.pkl",
]
```

## 📊 Database Schema

### User Account Model
```python
class Account(models.Model):
    user = OneToOneField(User)
    balance = DecimalField(12, 2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

## 🐛 Troubleshooting

### Model Not Loading
- Check model file path exists
- Verify joblib installation: `pip install joblib`
- System will use fallback formula if model missing

### Template Not Found
- Ensure templates are in `Banking/templates/banking/`
- Check TEMPLATES setting in `settings.py`

### Database Errors
- Run migrations: `python manage.py migrate`
- Check database file permissions

### Import Errors
- Verify `sys.path.insert()` points to correct finance_tools directory
- Check `__init__.py` files exist in all packages

## 📦 Dependencies

```
Django==4.2.0
joblib==1.3.0
numpy==1.24.0
scikit-learn==1.3.0
pandas==2.0.0
```

Install all:
```bash
pip install -r requirements.txt
```

## 🎓 Learning Outcomes

- Full-stack Django development
- User authentication & authorization
- Database design & ORM
- RESTful API design
- Machine learning integration
- Unit testing & test-driven development
- HTML/CSS/Bootstrap frontend
- Form handling & validation

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| POST | `/register/` | User registration |
| POST | `/login/` | User login |
| GET | `/dashboard/` | User dashboard |
| POST | `/deposit/` | Deposit funds |
| POST | `/withdraw/` | Withdraw funds |
| POST | `/calculator/<tool>/` | Run calculator |
| GET/POST | `/loan-estimator/` | ML loan predictor |

## 👨‍💻 Development Team

- **Project**: Smart Banking System - Full Stack Development
- **Framework**: Django 4.2
- **Database**: SQLite
- **ML Model**: Random Forest Regressor
- **Frontend**: Bootstrap 5

## 📄 License

This project is for educational purposes only.

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn ML Guide](https://scikit-learn.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Python Finance Calculations](https://pypi.org/)

## ✅ Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Run `python manage.py collectstatic`
- [ ] Set up proper logging
- [ ] Configure HTTPS
- [ ] Use production database (PostgreSQL)
- [ ] Run security checks: `python manage.py check --deploy`

## 📞 Support

For issues or questions:
1. Check test results: `python manage.py test -v 2`
2. Review error logs in terminal
3. Verify all dependencies installed
4. Check database migrations status

---

**Last Updated**: December 4, 2025  
**Status**: ✅ Fully Functional