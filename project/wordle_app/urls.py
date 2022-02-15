from django.urls import path
from .views import (
    GameCreateView,
    homepage,
    GameUpdateView,
    basic_form,
    class_form,
    multi_value_form,
    refactor,
)

app_name = "wordle_app"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("basic_form/", basic_form, name="basic_form"),
    path("class_form/", class_form, name="class_form"),
    path("multi_value_form/", multi_value_form, name="multi_value_form"),
    path("refactor", refactor, name="refactor"),
    path("create", GameCreateView.as_view(), name="create"),
    path("game/<str:pk>/", GameUpdateView.as_view(), name="game"),
    path("game/<str:pk>/attempt", GameUpdateView.as_view(), name="attempt"),
]
