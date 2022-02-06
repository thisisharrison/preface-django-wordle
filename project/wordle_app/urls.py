from django.urls import path
from .views import homepage

app_name = "wordle_app"

urlpatterns = [
    path("", homepage, name="homepage"),
]
