from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from wordle_word.models import Word

from wordle_app import forms
from .models import Game
from .utils import transform_data, next_game_time, is_same_date
import pdb

# Create your views here.


@login_required(login_url="/account/login/")
def homepage(request):
    [curr_date, next_game] = next_game_time()
    try:
        game = Game.objects.filter(player=request.user.id).latest("created_at")
    except Game.DoesNotExist:
        game = None

    # If user has no game OR game does not equal to today's date, start new game
    if game is None or not is_same_date(game.created_at, curr_date):
        game = Game.start_new_game(request)

    # user has a game, check if it's finished
    elif game.won != None:
        messages.add_message(request, messages.INFO, f"{next_game.seconds}")

    return redirect("wordle_app:game", game.id)


class GameUpdateView(UpdateView):
    model = Game
    fields = ["attempts", "won", "tries"]
    template_name = "wordle_app/index.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if not self.object.is_valid():
                self.object = Game.start_new_game(request)
                kwargs["pk"] = self.object.id
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect("wordle_app:homepage")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()

        attempt = ""
        for k, v in request.POST.items():
            if "char" in k:
                attempt += v.upper()

        if len(attempt) < 5:
            messages.add_message(request, messages.ERROR, "Not enough letters")
            return redirect(self.object.get_absolute_url())

        elif not Word.valid_word(attempt):
            messages.add_message(request, messages.ERROR, f'"{attempt}" not in word list')
            return redirect(self.object.get_absolute_url())

        else:
            prefix = self.object.attempts + "," if self.object.attempts else ""
            request.POST["attempts"] = prefix + attempt
            request.POST["tries"] = self.object.tries + 1
            request.POST["won"] = (
                True
                if self.object.word.word == attempt
                else False
                if request.POST["tries"] == 6
                else None
            )

            return super(GameUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = self.object.word.word
        attempts = self.object.attempts
        won = self.object.won
        [attempts_list, keyboard_list] = transform_data(word, attempts)
        context["attempts_list"] = attempts_list
        context["keyboard_list"] = keyboard_list
        context["remaining_attempts"] = (
            range(6 - len(attempts_list)) if len(attempts_list) >= 1 else range(6)
        )
        context["won"] = won
        return context

    # If submitted more than 6 attempts in a 5 letter game
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if response.status_code != 200 or form.errors:
            return self.render_to_response(
                self.get_context_data(form=form, errors=form.errors)
            )


""" ALTERNATIVE WAYS """

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
