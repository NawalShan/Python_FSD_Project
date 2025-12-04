from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Account


class BankingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass1234"
        )
        self.account = Account.objects.create(user=self.user, balance=1000)

    def test_user_registration(self):
        response = self.client.post(reverse("banking:register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_success(self):
        response = self.client.post(reverse("banking:login"), {
            "username": "testuser",
            "password": "pass1234",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_invalid(self):
        response = self.client.post(reverse("banking:login"), {
            "username": "testuser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_deposit(self):
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:deposit"), {"amount": 500})
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw_success(self):
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:withdraw"), {"amount": 300})
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_insufficient_balance(self):
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:withdraw"), {"amount": 5000})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insufficient balance")

    # ---------- Calculator Tests ----------
    def test_calculator_emi(self):
        """Test EMI (Equated Monthly Installment) Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["emi"]), {
            "principal": 1000000,
            "annual_rate": 10,
            "tenure": 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "emi")

    def test_calculator_sip(self):
        """Test SIP (Systematic Investment Plan) Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["sip"]), {
            "monthly": 5000,
            "annual_rate": 12,
            "years": 10,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sip")

    def test_calculator_fd(self):
        """Test FD (Fixed Deposit) Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["fd"]), {
            "principal": 100000,
            "annual_rate": 8,
            "years": 3,
            "freq": 4,  # quarterly
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fd")

    def test_calculator_rd(self):
        """Test RD (Recurring Deposit) Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["rd"]), {
            "monthly": 10000,
            "annual_rate": 7,
            "years": 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rd")

    def test_calculator_retirement(self):
        """Test Retirement Corpus Estimator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["retirement"]), {
            "savings": 500000,
            "monthly_add": 10000,
            "annual_return": 12,
            "years": 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "retirement")

    def test_calculator_eligibility(self):
        """Test Home Loan Eligibility Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["eligibility"]), {
            "income": 1000000,
            "expenses": 50000,
            "annual_rate": 8.5,
            "tenure": 20,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "eligibility")

    def test_calculator_credit_card(self):
        """Test Credit Card Balance Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["credit"]), {
            "balance": 50000,
            "monthly_interest": 2.5,
            "minimum_percent": 5,
            "months": 12,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "credit")

    def test_calculator_tax(self):
        """Test Income Tax Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["tax"]), {
            "gross": 1500000,
            "standard": 50000,
            "other": 0,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tax")

    def test_calculator_budget(self):
        """Test Budget Planner"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["budget"]), {
            "income": 100000,
            "expenses": 60000,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "budget")

    def test_calculator_networth(self):
        """Test Net Worth Calculator"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["networth"]), {
            "assets": "500000,200000,100000",
            "liabilities": "50000,25000",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "networth")

    def test_calculator_invalid_tool(self):
        """Test invalid calculator tool"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:calculator", args=["invalid"]), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown calculator tool")

    # ---------- Loan Estimator Tests ----------
    def test_loan_estimator_get(self):
        """Test loan estimator form display"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.get(reverse("banking:loan_estimator"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Loan Eligibility")

    def test_loan_estimator_post(self):
        """Test loan estimator prediction"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:loan_estimator"), {
            "age": 32,
            "income": 85000,
            "credit_score": 720,
            "tenure": 10,
            "existing_loan": 100000,
            "dependents": 2,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "result-box" in response.content.decode() or 
            "error-box" in response.content.decode()
        )
        self.assertContains(response, "32")
        self.assertContains(response, "85000")

    def test_loan_estimator_minimal_input(self):
        """Test loan estimator with minimal input"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:loan_estimator"), {
            "age": 25,
            "income": 50000,
            "credit_score": 650,
            "tenure": 15,
        })
        self.assertEqual(response.status_code, 200)

    def test_loan_estimator_high_income(self):
        """Test loan estimator with high income"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(reverse("banking:loan_estimator"), {
            "age": 40,
            "income": 500000,
            "credit_score": 800,
            "tenure": 20,
            "existing_loan": 0,
            "dependents": 0,
        })
        self.assertEqual(response.status_code, 200)

    # ---------- Authentication Tests ----------
    def test_logout(self):
        """Test logout functionality"""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.get(reverse("banking:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_protected_views_require_login(self):
        """Test that protected views require authentication"""
        protected_urls = [
            reverse("banking:dashboard"),
            reverse("banking:deposit"),
            reverse("banking:withdraw"),
            reverse("banking:loan_estimator"),
            reverse("banking:calculator", args=["emi"]),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # redirect to login
            self.assertIn("/login/", response.url)
