import pdb
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import UpdateView
from django.contrib import messages
from .models import Game

# Create your views here.


def homepage(request):
    # See if user is playing a valid game first
    try:
        game = Game.objects.filter(player=request.user.id).latest("created_at")
        if not game.is_valid():
            raise "Game expired, start new game"
    except ObjectDoesNotExist:
        # Otherwise create game for user
        game = Game.start_game(request)
    return render(
        request,
        "wordle_app/index.html",
        context={"game": game, "types": ["correct", "present", "absent"]},
    )


class GameUpdateView(UpdateView):
    model = Game
    fields = ["attempts"]
    template_name = "wordle_app/index.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        prefix = self.object.attempts + "," if self.object.attempts else ""
        request.POST["attempts"] = prefix + request.POST["attempts"]

        return super(GameUpdateView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if response.status_code is not 200 or form.errors:
            return self.render_to_response(
                self.get_context_data(form=form, errors=form.errors)
            )
