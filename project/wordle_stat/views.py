import pdb
from django.shortcuts import render, redirect
from django.utils import timezone, timesince
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from wordle_app.models import Game
from wordle_app.utils import is_same_date, next_game_time, transform_data


# Create your views here.


@login_required(login_url="/account/login/")
def stat(request):
    stat_context = {
        "distribution": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        },
        "played": 0,
        "win_rate": 0,
        "current_streak": 0,
        "max_streak": 0,
    }

    player = Game.objects.filter(player__exact=request.user.id).exclude(won__isnull=True)
    stat_context["played"] = player.count()

    if stat_context["played"] == 0:
        messages.add_message(request, messages.ERROR, "'No game stats'")
        return redirect("wordle_app:homepage")

    won = player.filter(won=True)
    stat_context["win_rate"] = (won.count() / stat_context["played"]) * 100

    # https://stackoverflow.com/questions/37205793/django-values-list-vs-values
    wins = list(won.values_list("tries", flat=True))
    max_value = 0
    for k in stat_context["distribution"]:
        stat_context["distribution"][k] = wins.count(k)
        max_value = max(stat_context["distribution"][k], max_value)

    streaks = list(won.values_list("created_at", flat=True).order_by("-created_at"))

    if not is_same_date(streaks[0], timezone.localtime()):
        stat_context["current_streak"] = 0
    else:
        for i, streak in enumerate(streaks):
            if i == 0:
                stat_context["current_streak"] += 1

            elif (streaks[i - 1] - streak).days == 1:
                stat_context["current_streak"] += 1

            else:
                break

    runner = 0
    max_count = 0

    for i, el in enumerate(streaks):
        if i == 0:
            runner += 1
        elif (streaks[i - 1] - el).days == 1:
            runner += 1
        else:
            max_count = runner if runner > max_count else max_count
            runner = 1

    max_count = runner if runner > max_count else max_count
    stat_context["max_streak"] = max_count

    try:
        last_game = Game.objects.filter(player=request.user.id).latest("created_at")
    except Game.DoesNotExist:
        last_game = None

    if last_game:
        attempts = last_game.attempts
        word = last_game.word.word
        [attempts_list, _] = transform_data(word, attempts)
        for i, row in enumerate(attempts_list):
            attempts_list[i] = list(map(lambda char: char[1], row))

    [_, next_game] = next_game_time()

    return render(
        request,
        "wordle_stat/index.html",
        {
            "stat": stat_context,
            "max_value": max_value,
            "squares": attempts_list,
            "last_game": last_game,
            "next_game": next_game.seconds,
        },
    )
