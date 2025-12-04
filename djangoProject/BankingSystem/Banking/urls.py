from django.urls import path
from . import views

app_name = "banking"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("deposit/", views.deposit_view, name="deposit"),
    path("withdraw/", views.withdraw_view, name="withdraw"),
    path("calculator/<str:tool>/", views.calculator_view, name="calculator"),
    path("loan-estimator/", views.loan_estimator, name="loan_estimator"),

]