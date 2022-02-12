import pdb
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import UpdateView
from django.contrib import messages

from wordle_word.models import Word

from wordle_app import forms
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


# How we want to break up each fields
def basic_form(request):
    form = forms.AttemptBasicForm()
    return render(request, "wordle_app/form.html", {"form": form})


# How to use class
def class_form(request):
    form = forms.AttemptClassForm()
    if request.POST:
        attempt = forms.AttemptClassForm(request.POST)
        if not attempt.is_valid():
            return render(request, "wordle_app/form.html", {"form": attempt})
        else:
            return HttpResponse("working")
    else:
        return render(request, "wordle_app/form.html", {"form": form})


# Not working
def multi_value_form(request):
    form = forms.AttemptMultiValueForm()
    return render(request, "wordle_app/form.html", {"form": form})


class GameUpdateView(UpdateView):
    model = Game
    fields = ["attempts"]
    template_name = "wordle_app/index.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_valid():
            self.object = Game.start_game(request)
            kwargs["pk"] = self.object.id
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()

        attempt = ""
        for k, v in request.POST.items():
            if "char" in k:
                attempt += v

        if len(attempt) < 5:
            messages.add_message(request, messages.ERROR, "Not enough letters")
            return redirect(self.object.get_absolute_url())

        elif not Word.valid_word(attempt):
            messages.add_message(request, messages.ERROR, "Not in word list")
            return redirect(self.object.get_absolute_url())

        else:
            prefix = self.object.attempts + "," if self.object.attempts else ""
            request.POST["attempts"] = (prefix + attempt).upper()
            request.POST["tries"] = self.object.tries + 1

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

    # If submitted more than 6 attempts in a 5 letter game
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if response.status_code != 200 or form.errors:
            return self.render_to_response(
                self.get_context_data(form=form, errors=form.errors)
            )
