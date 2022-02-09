import pdb
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import UpdateView
from django.contrib import messages

from .models import Game
from .utils import transform_data

# Create your views here.


class ExpiredGameException(Exception):
    pass


# If user is logged in, redirect to valid game (old or new)
# If user is not logged in, return index
def homepage(request):
    try:
        game = Game.objects.filter(player=request.user.id).latest("created_at")
        if not game.is_valid():
            # TODO: not getting to except clause
            # raise ExpiredGameException("Game has expired")
            pass
    except ObjectDoesNotExist or ExpiredGameException:
        # Otherwise create game for user
        game = Game.start_game(request)
    return redirect("wordle_app:game", game.id)

    # # For not logged in users:
    # return render(
    #     request,
    #     "wordle_app/index.html",
    #     context={"game": game},
    # )


class GameUpdateView(UpdateView):
    model = Game
    fields = ["attempts"]
    template_name = "wordle_app/index.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_valid():
            self.object = Game.start_game(request)
            pdb.set_trace()
            kwargs["pk"] = self.object.id
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        attempt = ""
        for k, v in request.POST.items():
            if "char" in k:
                attempt += v
        prefix = self.object.attempts + "," if self.object.attempts else ""
        request.POST["attempts"] = prefix + attempt
        # TODO: Increment tries

        return super(GameUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = self.object.word.word
        attempts = self.object.attempts
        [attempts_list, keyboard_list] = transform_data(word, attempts)
        context["attempts_list"] = attempts_list
        context["keyboard_list"] = keyboard_list
        context["remaining_attempts"] = (
            range(6 - len(attempts_list)) if len(attempts_list) >= 1 else range(6)
        )
        return context

    # TODO: Invalid based on word length (to scale up to more than 5 characters words)
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if response.status_code is not 200 or form.errors:
            return self.render_to_response(
                self.get_context_data(form=form, errors=form.errors)
            )
