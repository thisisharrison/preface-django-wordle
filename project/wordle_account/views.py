from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from wordle_account.models import CustomUser
from wordle_account.forms import CustomUserCreationForm

# Create your views here.
class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def random(request):
    user = CustomUser.random_preface_user()
    login(request, user)
    return redirect("wordle_app:homepage")
