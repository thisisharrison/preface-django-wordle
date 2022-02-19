from django.urls import path
from wordle_account.views import SignupView, random

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("random/", random, name="random"),
]
