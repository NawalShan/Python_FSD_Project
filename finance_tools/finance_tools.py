"""
finance_tools.py

A collection of simple, well-documented personal finance helper functions.

Each function:
 - validates inputs (raises ValueError / TypeError for invalid input)
 - returns numeric results (does not print)
 - uses clear docstrings describing parameters and return values
"""
from typing import Dict, List, Tuple
import math


def _to_float(name: str, value):
    """Convert to float and validate type."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"{name} must be a number")
    return v


def calculate_emi(principal, annual_rate_percent, tenure_years):
    """
    Calculate monthly EMI for a loan.

    Args:
        principal (float|int): loan principal > 0
        annual_rate_percent (float|int): annual interest rate in percent (>= 0)
        tenure_years (float|int): tenure in years (> 0)

    Returns:
        float: monthly EMI rounded to 2 decimals
    """
    P = _to_float("principal", principal)
    r_ann = _to_float("annual_rate_percent", annual_rate_percent)
    t = _to_float("tenure_years", tenure_years)

    if P <= 0:
        raise ValueError("principal must be > 0")
    if t <= 0:
        raise ValueError("tenure_years must be > 0")
    if r_ann < 0:
        raise ValueError("annual_rate_percent cannot be negative")

    monthly_rate = r_ann / 100.0 / 12.0
    n = int(round(t * 12))

    if monthly_rate == 0:
        emi = P / n
    else:
        emi = P * monthly_rate * (1 + monthly_rate) ** n / ((1 + monthly_rate) ** n - 1)

    return round(emi, 2)


def calculate_sip(monthly_investment, annual_return_percent, years):
    """
    Calculate SIP maturity amount (monthly contributions).

    Formula uses future value of an annuity with monthly compounding.

    Args:
        monthly_investment (float): monthly investment amount >= 0
        annual_return_percent (float): expected annual return % >= 0
        years (float): investment period in years > 0

    Returns:
        float: maturity amount rounded to 2 decimals
    """
    m = _to_float("monthly_investment", monthly_investment)
    r_ann = _to_float("annual_return_percent", annual_return_percent)
    y = _to_float("years", years)
    if m < 0:
        raise ValueError("monthly_investment cannot be negative")
    if y <= 0:
        raise ValueError("years must be > 0")
    if r_ann < 0:
        raise ValueError("annual_return_percent cannot be negative")

    monthly_rate = r_ann / 100.0 / 12.0
    n = int(round(y * 12))
    if monthly_rate == 0:
        amount = m * n
    else:
        amount = m * (((1 + monthly_rate) ** n - 1) / monthly_rate) * (1 + monthly_rate)

    return round(amount, 2)


def calculate_fd(principal, annual_rate_percent, years, compounding_frequency_per_year=1):
    """
    Calculate maturity amount for a lump-sum Fixed Deposit.

    Args:
        principal (float): initial amount > 0
        annual_rate_percent (float): annual rate % >= 0
        years (float): number of years > 0
        compounding_frequency_per_year (int): times interest compounds per year (1,2,4,12, etc.)

    Returns:
        float: maturity amount rounded to 2 decimals
    """
    P = _to_float("principal", principal)
    r = _to_float("annual_rate_percent", annual_rate_percent)
    t = _to_float("years", years)
    freq = int(compounding_frequency_per_year)
    if P <= 0:
        raise ValueError("principal must be > 0")
    if t <= 0:
        raise ValueError("years must be > 0")
    if r < 0:
        raise ValueError("annual_rate_percent cannot be negative")
    if freq <= 0:
        raise ValueError("compounding_frequency_per_year must be > 0")

    amount = P * (1 + r / 100.0 / freq) ** (freq * t)
    return round(amount, 2)


def calculate_rd(monthly_deposit, annual_rate_percent, years):
    """
    Calculate maturity value for a Recurring Deposit (monthly deposit).

    Uses approximate formula:
        M = P * n + interest, where interest ≈ monthly_deposit * n*(n+1)/2 * r_monthly

    Args:
        monthly_deposit (float): monthly deposit >= 0
        annual_rate_percent (float): annual rate % >= 0
        years (float): tenure in years > 0

    Returns:
        float: maturity amount rounded to 2 decimals
    """
    p = _to_float("monthly_deposit", monthly_deposit)
    r = _to_float("annual_rate_percent", annual_rate_percent)
    y = _to_float("years", years)
    if p < 0:
        raise ValueError("monthly_deposit cannot be negative")
    if y <= 0:
        raise ValueError("years must be > 0")
    if r < 0:
        raise ValueError("annual_rate_percent cannot be negative")

    n = int(round(y * 12))
    monthly_rate = r / 100.0 / 12.0

    if monthly_rate == 0:
        amount = p * n
    else:
        # Exact FV formula for monthly installments at monthly_rate (ordinary annuity)
        amount = p * (((1 + monthly_rate) ** n - 1) / monthly_rate) * (1 + monthly_rate)

    return round(amount, 2)


def estimate_retirement_corpus(current_savings, monthly_addition, annual_return_percent, years_to_retirement):
    """
    Estimate future retirement corpus using monthly contributions and compounding.

    Args:
        current_savings (float): existing savings >= 0
        monthly_addition (float): monthly contribution >= 0
        annual_return_percent (float): expected annual return % >= 0
        years_to_retirement (float): years left > 0

    Returns:
        float: estimated corpus rounded to 2 decimals
    """
    S = _to_float("current_savings", current_savings)
    add = _to_float("monthly_addition", monthly_addition)
    r = _to_float("annual_return_percent", annual_return_percent)
    y = _to_float("years_to_retirement", years_to_retirement)
    if S < 0 or add < 0:
        raise ValueError("savings and monthly additions cannot be negative")
    if y <= 0:
        raise ValueError("years_to_retirement must be > 0")
    if r < 0:
        raise ValueError("annual_return_percent cannot be negative")

    monthly_rate = r / 100.0 / 12.0
    n = int(round(y * 12))
    # Future value of current savings
    fv_savings = S * (1 + monthly_rate) ** n
    # Future value of series of monthly additions (ordinary annuity)
    if monthly_rate == 0:
        fv_additions = add * n
    else:
        fv_additions = add * (((1 + monthly_rate) ** n - 1) / monthly_rate) * (1 + monthly_rate)
    total = fv_savings + fv_additions
    return round(total, 2)


def estimate_home_loan_eligibility(monthly_income, monthly_expenses, interest_rate_percent, tenure_years, max_emi_percent=50):
    """
    Estimate maximum eligible loan principal using simple affordability rule.

    Assumptions:
      - Banks often allow EMI up to max_emi_percent of monthly income (default 50%).
      - Given that maximum EMI allowed = (monthly_income - monthly_expenses) capped by max_emi_percent * monthly_income.

    Args:
      monthly_income (float): gross monthly income >= 0
      monthly_expenses (float): monthly expenses >= 0
      interest_rate_percent (float): annual interest rate for loan in % >= 0
      tenure_years (float): loan tenure in years > 0
      max_emi_percent (float): fraction percent of income banks allow for EMI (0-100)

    Returns:
      float: estimated maximum loan principal rounded to 2 decimals
    """
    mi = _to_float("monthly_income", monthly_income)
    me = _to_float("monthly_expenses", monthly_expenses)
    r = _to_float("interest_rate_percent", interest_rate_percent)
    t = _to_float("tenure_years", tenure_years)
    mpe = _to_float("max_emi_percent", max_emi_percent)

    if mi < 0 or me < 0:
        raise ValueError("income/expenses cannot be negative")
    if t <= 0:
        raise ValueError("tenure_years must be > 0")
    if r < 0:
        raise ValueError("interest_rate_percent cannot be negative")
    if not (0 <= mpe <= 100):
        raise ValueError("max_emi_percent must be between 0 and 100")

    disposable = max(0.0, mi - me)
    emi_cap = min(disposable, mi * (mpe / 100.0))
    # Invert EMI formula to get principal: P = EMI * ( (1+r)^n -1 ) / (r*(1+r)^n )
    monthly_rate = r / 100.0 / 12.0
    n = int(round(t * 12))
    if n <= 0:
        raise ValueError("tenure in months must be > 0")

    if monthly_rate == 0:
        principal = emi_cap * n
    else:
        factor = ((1 + monthly_rate) ** n - 1) / (monthly_rate * (1 + monthly_rate) ** n)
        principal = emi_cap * factor

    return round(principal, 2)


def calculate_credit_card_balance(current_balance, monthly_interest_percent, minimum_payment_percent, months):
    """
    Estimate outstanding credit card balance if only minimum payments are made.

    This uses a month-by-month iterative model:
      - Each month: interest applied, then minimum payment paid.

    Args:
      current_balance (float): outstanding balance >= 0
      monthly_interest_percent (float): monthly interest rate in % >= 0
      minimum_payment_percent (float): minimum payment as % of balance (e.g., 5)
      months (int): number of months to simulate >= 1

    Returns:
      float: remaining balance after 'months' months rounded to 2 decimals
    """
    bal = _to_float("current_balance", current_balance)
    mi = _to_float("monthly_interest_percent", monthly_interest_percent)
    mp = _to_float("minimum_payment_percent", minimum_payment_percent)
    m = int(_to_float("months", months))
    if bal < 0:
        raise ValueError("current_balance cannot be negative")
    if mi < 0 or mp < 0:
        raise ValueError("rates cannot be negative")
    if m < 1:
        raise ValueError("months must be >= 1")

    monthly_rate = mi / 100.0
    for _ in range(m):
        # interest
        bal = bal * (1 + monthly_rate)
        # minimum payment
        payment = bal * (mp / 100.0)
        # if payment exceeds balance, zero it
        bal = max(0.0, bal - payment)

    return round(bal, 2)


def calculate_taxable_income(gross_income_yearly, standard_deduction=50000, other_deductions=0):
    """
    Calculate yearly taxable income after standard deduction and optional other deductions.

    Args:
      gross_income_yearly (float): gross annual income >= 0
      standard_deduction (float): standard deduction amount >= 0
      other_deductions (float): other allowed deductions >= 0

    Returns:
      float: taxable income (>= 0) rounded to 2 decimals
    """
    gi = _to_float("gross_income_yearly", gross_income_yearly)
    sd = _to_float("standard_deduction", standard_deduction)
    od = _to_float("other_deductions", other_deductions)
    if gi < 0 or sd < 0 or od < 0:
        raise ValueError("income/deductions cannot be negative")

    taxable = max(0.0, gi - sd - od)
    return round(taxable, 2)


def plan_budget(monthly_income, monthly_expenses):
    """
    Provide a simple budget recommendation.

    Returns:
      dict: {
        'savings_target': recommended monthly savings,
        'recommended_savings_percent': percent of income,
        'surplus_or_deficit': monthly_income - monthly_expenses
      }

    Logic:
      - If expenses <= 70% of income -> recommend savings = 20% of income.
      - Else if expenses <= 90% -> recommend 10% savings.
      - Else recommend trimming expenses or 0% savings.
    """
    mi = _to_float("monthly_income", monthly_income)
    me = _to_float("monthly_expenses", monthly_expenses)
    if mi < 0 or me < 0:
        raise ValueError("income/expenses cannot be negative")

    surplus = mi - me
    if mi == 0:
        rec_percent = 0.0
    else:
        expense_ratio = me / mi
        if expense_ratio <= 0.7:
            rec_percent = 20.0
        elif expense_ratio <= 0.9:
            rec_percent = 10.0
        else:
            rec_percent = 0.0

    savings_target = round(mi * (rec_percent / 100.0), 2)
    return {
        "savings_target": savings_target,
        "recommended_savings_percent": rec_percent,
        "surplus_or_deficit": round(surplus, 2),
    }


def calculate_net_worth(assets: List[float], liabilities: List[float]):
    """
    Compute net worth = sum(assets) - sum(liabilities).

    Args:
      assets (list of numbers): asset values >= 0
      liabilities (list of numbers): liability values >= 0

    Returns:
      float: net worth rounded to 2 decimals
    """
    if not isinstance(assets, (list, tuple)) or not isinstance(liabilities, (list, tuple)):
        raise TypeError("assets and liabilities must be lists or tuples")
    total_assets = 0.0
    total_liabilities = 0.0
    for i, a in enumerate(assets):
        a_f = _to_float(f"asset_{i}", a)
        if a_f < 0:
            raise ValueError("asset values cannot be negative")
        total_assets += a_f
    for i, l in enumerate(liabilities):
        l_f = _to_float(f"liability_{i}", l)
        if l_f < 0:
            raise ValueError("liability values cannot be negative")
        total_liabilities += l_f
    net = total_assets - total_liabilities
    return round(net, 2)
