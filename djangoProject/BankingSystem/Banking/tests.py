from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Account


class BankingTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass1234"
        )
        self.account = Account.objects.create(user=self.user, balance=1000)


    # ----------------------------
    # Registration Tests
    # ----------------------------
    def test_user_registration(self):
        response = self.client.post(reverse("banking:register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123",
        })

        self.assertEqual(response.status_code, 302)  # redirected
        self.assertTrue(User.objects.filter(username="newuser").exists())


    # ----------------------------
    # Login Tests
    # ----------------------------
    def test_login_success(self):
        response = self.client.post(reverse("banking:login"), {
            "username": "testuser",
            "password": "pass1234",
        })
        self.assertEqual(response.status_code, 302)   # dashboard
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_invalid(self):
        response = self.client.post(reverse("banking:login"), {
            "username": "testuser",
            "password": "wrongpass",
        })
        self.assertContains(response, "Invalid username or password")


    # ----------------------------
    # Deposit Tests
    # ----------------------------
    def test_deposit(self):
        self.client.login(username="testuser", password="pass1234")

        response = self.client.post(reverse("banking:deposit"), {
            "amount": 500,
        })

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1500)


    # ----------------------------
    # Withdraw Tests
    # ----------------------------
    def test_withdraw_success(self):
        self.client.login(username="testuser", password="pass1234")

        response = self.client.post(reverse("banking:withdraw"), {
            "amount": 300,
        })

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_insufficient_balance(self):
        self.client.login(username="testuser", password="pass1234")

        response = self.client.post(reverse("banking:withdraw"), {
            "amount": 5000,
        })

        self.assertContains(response, "Insufficient balance")


    # ----------------------------
    # Calculator Tests (EMI Example)
    # ----------------------------
    def test_calculator_emi(self):
        self.client.login(username="testuser", password="pass1234")

        response = self.client.post(reverse("banking:calculator", args=["emi"]), {
            "principal": 100000,
            "annual_rate": 10,
            "tenure": 1
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Result")
