from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class DepositForm(forms.Form):
    amount = forms.FloatField(min_value=0.01)


class WithdrawForm(forms.Form):
    amount = forms.FloatField(min_value=0.01)


class CalculatorForm(forms.Form):
    """
    Dynamic multi-tool calculator form.
    Each tool uses only the fields it needs.
    """

    TOOL_CHOICES = [
        ("emi", "EMI Calculator"),
        ("sip", "SIP Calculator"),
        ("fd", "Fixed Deposit Calculator"),
        ("rd", "Recurring Deposit Calculator"),
        ("retirement", "Retirement Savings Estimator"),
        ("eligibility", "Home Loan Eligibility"),
        ("credit", "Credit Card Interest Calculator"),
        ("tax", "Taxable Income Calculator"),
        ("budget", "Simple Budget Planner"),
        ("networth", "Net Worth Calculator"),
    ]

    tool = forms.ChoiceField(choices=TOOL_CHOICES)

    # Common fields reused across tools
    principal = forms.FloatField(required=False)
    annual_rate = forms.FloatField(required=False)
    tenure = forms.FloatField(required=False)
    years = forms.FloatField(required=False)
    monthly = forms.FloatField(required=False)

    savings = forms.FloatField(required=False)
    monthly_add = forms.FloatField(required=False)
    annual_return = forms.FloatField(required=False)

    income = forms.FloatField(required=False)
    expenses = forms.FloatField(required=False)

    balance = forms.FloatField(required=False)
    monthly_interest = forms.FloatField(required=False)
    minimum_percent = forms.FloatField(required=False)
    months = forms.IntegerField(required=False)

    gross = forms.FloatField(required=False)
    standard = forms.FloatField(required=False)
    other = forms.FloatField(required=False)

    assets = forms.CharField(required=False)
    liabilities = forms.CharField(required=False)

class LoanForm(forms.Form):
    age = forms.IntegerField(min_value=18, max_value=100, initial=32)
    monthly_income = forms.FloatField(min_value=0, initial=85000)
    credit_score = forms.IntegerField(min_value=300, max_value=850, initial=720)
    loan_tenure_years = forms.IntegerField(min_value=1, max_value=30, initial=10)
    existing_loan_amount = forms.FloatField(min_value=0, initial=100000)
    num_of_dependents = forms.IntegerField(min_value=0, max_value=10, initial=2)