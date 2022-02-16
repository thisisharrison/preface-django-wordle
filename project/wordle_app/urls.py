from django.urls import path
from .views import GameCreateView, homepage, GameUpdateView, GameUpdateViewV2

app_name = "wordle_app"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("game/create", GameCreateView.as_view(), name="create"),
    path("game/v2/<str:pk>", GameUpdateViewV2.as_view(), name="gameV2"),
    path("game/v2/<str:pk>/attempt", GameUpdateViewV2.as_view(), name="attemptV2"),
    # deprecate
    path("game/v1/<str:pk>", GameUpdateView.as_view(), name="game"),
    path("game/v1/<str:pk>/attempt", GameUpdateView.as_view(), name="attempt"),
]
