from django.urls import path
from wordle_account.views import SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
