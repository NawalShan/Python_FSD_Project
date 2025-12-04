from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import RegisterForm, LoginForm, DepositForm, WithdrawForm, CalculatorForm,LoanForm
from .models import Account, LoanRequest
import joblib
import numpy as np
from django.http import JsonResponse
import sys
import os


# Path to finance_tools
finance_tools_path = r"C:\Users\249422\Desktop\Final-Fsd-project\finance_tools"
sys.path.insert(0, finance_tools_path)

# Import all calculators
from finance_tools import (
    calculate_emi,
    calculate_sip,
    calculate_fd,
    calculate_rd,
    estimate_retirement_corpus,
    estimate_home_loan_eligibility,
    calculate_credit_card_balance,
    calculate_taxable_income,
    plan_budget,
    calculate_net_worth,
)


def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            Account.objects.create(user=user, balance=0.0)
            return redirect("banking:login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("banking:dashboard")

            return render(request, "login.html", {"form": form, "error": "Invalid credentials"})

    return render(request, "login.html", {"form": LoginForm()})


def logout_view(request):
    logout(request)
    return redirect("banking:home")


@login_required
def dashboard(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    return render(request, "dashboard.html", {"account": account})


@login_required
def deposit_view(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            try:
                account.deposit(form.cleaned_data["amount"])
                return redirect("banking:dashboard")
            except Exception as e:
                return render(request, "deposit.html", {"form": form, "error": str(e)})

    return render(request, "deposit.html", {"form": DepositForm()})


@login_required
def withdraw_view(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            try:
                account.withdraw(form.cleaned_data["amount"])
                return redirect("banking:dashboard")
            except Exception as e:
                return render(request, "withdraw.html", {"form": form, "error": str(e)})

    return render(request, "withdraw.html", {"form": WithdrawForm()})


@login_required
def calculator_view(request, tool):
    result = None
    error = None

    if request.method == "POST":
        try:
            if tool == "emi":
                result = calculate_emi(
                    float(request.POST.get("principal")),
                    float(request.POST.get("annual_rate")),
                    float(request.POST.get("tenure")),
                )

            elif tool == "sip":
                result = calculate_sip(
                    float(request.POST.get("monthly")),
                    float(request.POST.get("annual_rate")),
                    float(request.POST.get("years")),
                )

            elif tool == "fd":
                result = calculate_fd(
                    float(request.POST.get("principal")),
                    float(request.POST.get("annual_rate")),
                    float(request.POST.get("years")),
                    int(request.POST.get("freq", 1)),
                )

            elif tool == "rd":
                result = calculate_rd(
                    float(request.POST.get("monthly")),
                    float(request.POST.get("annual_rate")),
                    float(request.POST.get("years")),
                )

            elif tool == "retirement":
                result = estimate_retirement_corpus(
                    float(request.POST.get("savings")),
                    float(request.POST.get("monthly_add")),
                    float(request.POST.get("annual_return")),
                    float(request.POST.get("years")),
                )

            elif tool == "eligibility":
                result = estimate_home_loan_eligibility(
                    float(request.POST.get("income")),
                    float(request.POST.get("expenses")),
                    float(request.POST.get("annual_rate")),
                    float(request.POST.get("tenure")),
                )

            elif tool == "credit":
                result = calculate_credit_card_balance(
                    float(request.POST.get("balance")),
                    float(request.POST.get("monthly_interest")),
                    float(request.POST.get("minimum_percent")),
                    int(request.POST.get("months")),
                )

            elif tool == "tax":
                result = calculate_taxable_income(
                    float(request.POST.get("gross")),
                    float(request.POST.get("standard")),
                    float(request.POST.get("other")),
                )

            elif tool == "budget":
                result = plan_budget(
                    float(request.POST.get("income")),
                    float(request.POST.get("expenses")),
                )

            elif tool == "networth":
                assets = [float(a) for a in request.POST.get("assets", "").split(",") if a.strip()]
                liabilities = [float(l) for l in request.POST.get("liabilities", "").split(",") if l.strip()]
                result = calculate_net_worth(assets, liabilities)

            else:
                error = "Unknown calculator tool."

        except Exception as e:
            error = str(e)

    return render(
        request,
        "calculator.html",
        {"tool": tool, "result": result, "error": error},
    )

# Load ML model
MODEL_PATH = r"C:\Users\249422\Desktop\Final-Fsd-project\loan_estimator_model\loan_tool_output\loan_amount_model.joblib"
model = None
try:
    model = joblib.load(MODEL_PATH)
    print(f"✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Model load failed: {e}")

@login_required
def predict_view(request):
    predicted = None
    error = None
    form = LoanForm()

    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                vec = np.array([
                    float(cd['age']),
                    float(cd['monthly_income']),
                    float(cd['credit_score']),
                    float(cd['loan_tenure_years']),
                    float(cd['existing_loan_amount']),
                    float(cd['num_of_dependents'])
                ]).reshape(1, -1)

                if model is not None:
                    predicted = float(model.predict(vec)[0])
                    print(f"✓ Prediction: {predicted}")
                else:
                    # Fallback formula
                    predicted = float(cd['monthly_income']) * 12 * 0.6
                    print(f"✓ Fallback estimate: {predicted}")

                LoanRequest.objects.create(
                    user=request.user,
                    age=cd['age'],
                    monthly_income=cd['monthly_income'],
                    credit_score=cd['credit_score'],
                    loan_tenure_years=cd['loan_tenure_years'],
                    existing_loan_amount=cd['existing_loan_amount'],
                    num_of_dependents=cd['num_of_dependents'],
                    predicted_amount=predicted
                )
            except Exception as e:
                error = f"Prediction error: {str(e)}"
                print(f"✗ Error: {error}")

    return render(request, "loanEstimator.html", {
        "form": form,
        "predicted": round(predicted, 2) if predicted else None,
        "error": error
    })