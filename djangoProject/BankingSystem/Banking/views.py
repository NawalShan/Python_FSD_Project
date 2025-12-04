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
    funcs = {
        "emi": lambda p, r, t: calculate_emi(p, r, t),
        "sip": lambda m, r, y: calculate_sip(m, r, y),
        "fd": lambda p, r, y, f: calculate_fd(p, r, y, f),
        "rd": lambda m, r, y: calculate_rd(m, r, y),
        "retirement": lambda s, a, r, y: estimate_retirement_corpus(s, a, r, y),
        "eligibility": lambda i, e, r, t: estimate_home_loan_eligibility(i, e, r, t),
        "credit": lambda b, mi, mp, m: calculate_credit_card_balance(b, mi, mp, m),
        "tax": lambda g, s, o: calculate_taxable_income(g, s, o),
        "budget": lambda i, e: plan_budget(i, e),
        "networth": lambda a, l: calculate_net_worth(a, l)
    }

    if request.method == "POST":
        try:
            if tool not in funcs:
                error = "Unknown calculator tool."
            elif tool == "networth":
                a = [float(x) for x in request.POST.get("assets", "").split(",") if x.strip()]
                l = [float(x) for x in request.POST.get("liabilities", "").split(",") if x.strip()]
                result = funcs["networth"](a, l)
            else:
                args = [float(v) for v in request.POST.values() if v]
                result = funcs[tool](*args)
        except Exception as e:
            error = str(e)

    return render(request, "calculator.html", {"tool": tool, "result": result, "error": error})

# ---------- Loan Estimator ----------
MODEL_PATHS = [
    r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_amount_estimation_model.pkl"
]

def load_model():
    for path in MODEL_PATHS:
        if os.path.exists(path):
            try:
                print(f"✓ Model loaded from: {path}")
                return joblib.load(path)
            except Exception as e:
                print(f"✗ Failed: {e}")
    print("✗ No model found. Using fallback.")
    return None

model = load_model()

@login_required
def loan_estimator(request):
    predicted, error = None, None
    form = LoanEstimatorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        X = np.array([[d["age"], d["income"], d["credit_score"],
                       d["tenure"], d.get("existing_loan", 0), d.get("dependents", 0)]])
        try:
            if model:
                predicted = float(model.predict(X)[0])
            else:
                predicted = max(0.0, (d["income"] * 12 * 0.6) - d.get("existing_loan", 0))
            predicted = round(predicted, 2)
        except Exception as e:
            error = f"Prediction error: {e}"

    return render(request, "loanEstimator.html", {
        "form": form,
        "predicted_amount": predicted,
        "error": error
    })
