from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from wordle_app import forms
from .models import Game
from .utils import keyboard_to_list, transform_data, next_game_time, is_same_date
import pdb

# Create your views here.


def homepage(request, exception=None):
    [curr_date, next_game] = next_game_time()
    try:
        game = Game.objects.filter(player=request.user.id).latest("created_at")
    except Game.DoesNotExist:
        game = None

    if game is None or not is_same_date(game.created_at, curr_date):
        return redirect("wordle_app:new")

    elif game.won != None:
        messages.add_message(request, messages.INFO, f"{next_game.seconds}")
    return redirect("wordle_app:game", game.id)


class GamePermissionMixin(UserPassesTestMixin):
    redirect_field_name = "wordle_app:homepage"

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, '"Not your game!"')
        return redirect(reverse(self.redirect_field_name))

    def test_func(self):
        return Game.objects.get(pk=self.kwargs["pk"]).player.id == self.request.user.id


class GameCreateView(CreateView):
    model = Game
    template_name = "wordle_app/index.html"
    form_class = forms.AttemptClassForm

    def get_form_kwargs(self):
        kwargs = super(GameCreateView, self).get_form_kwargs()
        kwargs.update({"type": "create"})
        return kwargs

    def get_success_url(self):
        return reverse("wordle_app:game", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, "Log In to play!")
            return redirect("login")
        form.instance.player = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempts_list"] = None
        context["keyboard_list"] = keyboard_to_list()
        context["remaining_attempts"] = range(6)
        return context


class GameUpdateView(LoginRequiredMixin, GamePermissionMixin, UpdateView):
    model = Game
    template_name = "wordle_app/index.html"
    form_class = forms.AttemptClassForm
    login_url = settings.LOGIN_URL

    def get_form_kwargs(self):
        kwargs = super(GameUpdateView, self).get_form_kwargs()
        kwargs.update({"type": "update"})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        word = self.object.word.word
        attempts = obj.attempts if context["form"].errors else self.object.attempts
        won = self.object.won
        [attempts_list, keyboard_list] = transform_data(word, attempts)
        context["attempts_list"] = attempts_list
        context["keyboard_list"] = keyboard_list
        context["remaining_attempts"] = (
            range(6 - len(attempts_list)) if len(attempts_list) >= 1 else range(6)
        )
        context["won"] = won

        # was previously filled with wrong inputs
        if context["form"].is_bound and context["form"].errors:
            pass
        # no errors and not bound
        else:
            context["form"] = self.form_class(type="update")

        if won:
            context["form"].fields["attempts"].widget.attrs["disabled"] = True
            congrats = [
                "Genius",
                "Magnificent",
                "Impressive",
                "Splendid",
                "Great",
                "Phew",
            ]
            if len(messages.get_messages(self.request)) == 0:
                messages.add_message(
                    self.request, messages.INFO, f"'{congrats[self.object.tries - 1]}!'"
                )
        elif won == False:
            msg = f'The word is "{word.upper()}"'
            messages.add_message(self.request, messages.INFO, f"'{msg}'")

        return context

    def get_success_url(self):
        id = self.kwargs["pk"]
        return reverse_lazy("wordle_app:game", kwargs={"pk": id})
