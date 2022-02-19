from django.urls import path
from .views import GameCreateView, homepage, GameUpdateView, GameUpdateView

app_name = "wordle_app"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("game/new", GameCreateView.as_view(), name="new"),
    path("game/<str:pk>", GameUpdateView.as_view(), name="game"),
]
