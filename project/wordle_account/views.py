from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from wordle_account.forms import CustomUserCreationForm

# Create your views here.
class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
