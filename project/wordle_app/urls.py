from django.urls import path
from .views import homepage, GameUpdateView

app_name = "wordle_app"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("<str:pk>/", GameUpdateView.as_view(), name="game"),
    path("<str:pk>/attempt", GameUpdateView.as_view(), name="attempt"),
]
