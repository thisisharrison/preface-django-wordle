from django.urls import path
from .views import (
    GameCreateView,
    homepage,
    GameUpdateView,
)

app_name = "wordle_app"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("create", GameCreateView.as_view(), name="create"),
    path("game/<str:pk>/", GameUpdateView.as_view(), name="game"),
    path("game/<str:pk>/attempt", GameUpdateView.as_view(), name="attempt"),
]
