from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import numpy as np




class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += Decimal(amount)
        self.save()

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if Decimal(amount) > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= Decimal(amount)
        self.save()

    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"

class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.PositiveIntegerField()
    monthly_income = models.FloatField()
    credit_score = models.PositiveIntegerField()
    loan_tenure_years = models.PositiveIntegerField()
    existing_loan_amount = models.FloatField(default=0.0)
    num_of_dependents = models.PositiveIntegerField(default=0)
    predicted_amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LoanRequest(id={self.id}, predicted=₹{self.predicted_amount})"
