from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from .forms import (
    RegisterForm, LoginForm, DepositForm, WithdrawForm,
    LoanEstimatorForm
)
from .models import Account
import os, sys, joblib, numpy as np

# --- Import custom finance tools ---
sys.path.insert(0, r"C:\Users\249422\Desktop\Final-Fsd-project\finance_tools")
from finance_tools import (
    calculate_emi, calculate_sip, calculate_fd, calculate_rd,
    estimate_retirement_corpus, estimate_home_loan_eligibility,
    calculate_credit_card_balance, calculate_taxable_income,
    plan_budget, calculate_net_worth
)

# ---------- Basic Views ----------
def home(request): 
    return render(request, "home.html")

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        Account.objects.create(user=user, balance=0.0)
        return redirect("banking:login")
    return render(request, "register.html", {"form": form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            return redirect("banking:dashboard")
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("banking:home")

@login_required
def dashboard(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    return render(request, "dashboard.html", {"account": account})

# ---------- Deposit / Withdraw ----------
@login_required
def deposit_view(request):
    account = Account.objects.get(user=request.user)
    form = DepositForm(request.POST or None)
    if form.is_valid():
        try:
            account.deposit(form.cleaned_data["amount"])
            return redirect("banking:dashboard")
        except Exception as e:
            return render(request, "deposit.html", {"form": form, "error": str(e)})
    return render(request, "deposit.html", {"form": form})

@login_required
def withdraw_view(request):
    account = Account.objects.get(user=request.user)
    form = WithdrawForm(request.POST or None)
    if form.is_valid():
        try:
            account.withdraw(form.cleaned_data["amount"])
            return redirect("banking:dashboard")
        except Exception as e:
            return render(request, "withdraw.html", {"form": form, "error": str(e)})
    return render(request, "withdraw.html", {"form": form})

# ---------- Finance Tools ----------
@login_required
def calculator_view(request, tool):
    result = error = None

    if request.method == "POST":
        try:
            if tool == "emi":
                principal = float(request.POST.get("principal", 0))
                annual_rate = float(request.POST.get("annual_rate", 0))
                tenure = float(request.POST.get("tenure", 0))
                result = calculate_emi(principal, annual_rate, tenure)

            elif tool == "sip":
                monthly = float(request.POST.get("monthly", 0))
                annual_rate = float(request.POST.get("annual_rate", 0))
                years = float(request.POST.get("years", 0))
                final_amount = calculate_sip(monthly, annual_rate, years)
                result = {
                    'total_investment': round(monthly * 12 * years, 2),
                    'final_amount': round(final_amount, 2),
                    'gains': round(final_amount - (monthly * 12 * years), 2)
                }

            elif tool == "fd":
                principal = float(request.POST.get("principal", 0))
                annual_rate = float(request.POST.get("annual_rate", 0))
                years = float(request.POST.get("years", 0))
                freq = int(request.POST.get("freq", 1))
                result = calculate_fd(principal, annual_rate, years, freq)

            elif tool == "rd":
                monthly = float(request.POST.get("monthly", 0))
                annual_rate = float(request.POST.get("annual_rate", 0))
                years = float(request.POST.get("years", 0))
                result = calculate_rd(monthly, annual_rate, years)

            elif tool == "retire":
                savings = float(request.POST.get("savings", 0))
                monthly_add = float(request.POST.get("monthly_add", 0))
                annual_return = float(request.POST.get("annual_return", 0))
                years = float(request.POST.get("years", 0))
                result = estimate_retirement_corpus(savings, monthly_add, annual_return, years)

            elif tool == "home":
                income = float(request.POST.get("income", 0))
                expenses = float(request.POST.get("expenses", 0))
                annual_rate = float(request.POST.get("annual_rate", 0))
                tenure = float(request.POST.get("tenure", 0))
                result = estimate_home_loan_eligibility(income, expenses, annual_rate, tenure)

            elif tool == "cc":
                balance = float(request.POST.get("balance", 0))
                monthly_interest = float(request.POST.get("monthly_interest", 0))
                minimum_percent = float(request.POST.get("minimum_percent", 0))
                months = int(request.POST.get("months", 0))
                cc_result = calculate_credit_card_balance(balance, monthly_interest, minimum_percent, months)
                result = {
                    'total_interest': round(cc_result.get('interest', 0), 2) if isinstance(cc_result, dict) else round(cc_result, 2),
                    'total_paid': round(balance + cc_result.get('interest', cc_result), 2) if isinstance(cc_result, dict) else round(balance + cc_result, 2)
                }

            elif tool == "tax":
                gross = float(request.POST.get("gross", 0))
                standard = float(request.POST.get("standard", 50000))
                other = float(request.POST.get("other", 0))
                result = calculate_taxable_income(gross, standard, other)

            elif tool == "budget":
                income = float(request.POST.get("income", 0))
                expenses = float(request.POST.get("expenses", 0))
                result = plan_budget(income, expenses)

            elif tool == "networth":
                assets = [float(x.strip()) for x in request.POST.get("assets", "").split(",") if x.strip()]
                liabilities = [float(x.strip()) for x in request.POST.get("liabilities", "").split(",") if x.strip()]
                result = calculate_net_worth(assets, liabilities)

            else:
                error = "Unknown calculator tool."

        except ValueError as e:
            error = f"Invalid input: Please enter valid numbers"
        except Exception as e:
            error = f"Calculation error: {str(e)}"

    return render(request, "calculator.html", {
        "tool": tool,
        "result": result,
        "error": error
    })

# ---------- Loan Estimator ----------
CANDIDATE_MODELS = [
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_tool_output\loan_amount_model.joblib",
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_amount_model.joblib",
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_amount_model.pkl",
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_amount_estimation_model.pkl",
]

def get_model():
    """Load ML model from candidate paths"""
    for model_path in CANDIDATE_MODELS:
        if os.path.exists(model_path):
            try:
                m = joblib.load(model_path)
                print(f"✓ Model loaded from: {model_path}")
                return m
            except Exception as e:
                print(f"✗ Failed to load {model_path}: {e}")
    print("✗ No model found. Using fallback estimation.")
    return None

model = get_model()

@login_required
def loan_estimator(request):
    predicted_amount = None
    error = None
    model_source = "fallback"
    form = LoanEstimatorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            d = form.cleaned_data
            age = float(d["age"])
            income = float(d["income"])
            credit_score = float(d["credit_score"])
            tenure = float(d["tenure"])
            existing_loan = float(d.get("existing_loan", 0) or 0)
            dependents = float(d.get("dependents", 0) or 0)

            # Create feature vector [age, income, credit_score, tenure, existing_loan, dependents]
            features = np.array([[age, income, credit_score, tenure, existing_loan, dependents]], dtype=float)

            if model is not None:
                try:
                    predicted_amount = float(model.predict(features)[0])
                    model_source = "ML Model"
                    print(f"✓ ML Prediction: {predicted_amount}")
                except Exception as e:
                    print(f"✗ Model prediction failed: {e}. Using fallback.")
                    predicted_amount = max(0.0, (income * 12 * 0.6) - existing_loan)
                    model_source = "fallback"
            else:
                # Fallback: 60% of annual income - existing loan
                predicted_amount = max(0.0, (income * 12 * 0.6) - existing_loan)
                model_source = "fallback"

            predicted_amount = round(predicted_amount, 2)

        except ValueError:
            error = "Please enter valid numeric values for all fields."
        except Exception as e:
            error = f"Prediction error: {str(e)}"

    return render(request, "loanEstimator.html", {
        "form": form,
        "predicted_amount": predicted_amount,
        "error": error,
        "model_source": model_source
    })
