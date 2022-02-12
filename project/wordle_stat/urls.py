from django.urls import path
from .views import stat

app_name = "wordle_stat"

urlpatterns = [
    path("", stat, name="stat"),
]
