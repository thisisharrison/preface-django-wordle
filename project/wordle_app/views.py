from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
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


class GameCreateView(CreateView):
    model = Game
    template_name = "wordle_app/form.html"
    form_class = forms.AttemptClassForm

    def get_form_kwargs(self):
        kwargs = super(GameCreateView, self).get_form_kwargs()
        kwargs.update({"player": self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("wordle_app:game", kwargs={"pk": self.object.id})

    # # Vanilla way:
    # def get(self, request, *args, **kwargs):
    #     context = {"form": forms.AttemptClassForm}
    #     return render(request, "wordle_app/form.html", {"form": form})

    # def post(self, request, *args, **kwargs):
    #     form = forms.AttemptClassForm(request.POST)
    #     if form.is_valid():
    #         return HttpResponse("ok")
    #     return render(request, "wordle_app/form.html", {"form": form})


class GameUpdateView(UpdateView):
    model = Game
    fields = ["attempts", "won", "tries"]
    template_name = "wordle_app/index.html"

    # Check if new games get accidentally created
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.player.id == request.user.id:
                return super().get(request, *args, **kwargs)
            else:
                # TODO: throw correct status code error
                raise Http404
        except Http404:
            return redirect("wordle_app:homepage")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        word = self.object.word.word
        attempt = ""

        for k, v in request.POST.items():
            if "char" in k:
                attempt += v.upper()

        if len(attempt) < 5:
            messages.add_message(request, messages.ERROR, '"Not enough letters"')
            return redirect(self.object.get_absolute_url())

        elif not Word.valid_word(attempt):
            msg = f'"{attempt}" not in word list'
            messages.add_message(request, messages.ERROR, f"'{msg}'")
            return redirect(self.object.get_absolute_url())

        else:
            prefix = self.object.attempts + "," if self.object.attempts else ""
            tries = self.object.tries + 1
            won = True if word == attempt else False if tries == 6 else None

            request.POST["attempts"] = prefix + attempt
            request.POST["tries"] = tries
            request.POST["won"] = won

            if won:
                congrats = [
                    "Genius",
                    "Magnificent",
                    "Impressive",
                    "Splendid",
                    "Great",
                    "Phew",
                ]
                messages.add_message(request, messages.INFO, f"'{congrats[tries - 1]}!'")
            elif won == False:
                msg = f'The word is "{word}"'
                messages.add_message(request, messages.INFO, f"'{msg}'")

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
