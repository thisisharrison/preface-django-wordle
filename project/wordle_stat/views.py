import pdb
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from wordle_app.models import Game
from wordle_app.utils import is_same_date, next_game_time, transform_data


# Create your views here.
# https://nerdschalk.com/average-wordle-score-and-stats-what-are-they-and-how-to-find-some/


@login_required(login_url="/account/login/")
def stat(request):
    stat_context = {
        "distribution": {  # How many words guesses you used how many times in all the WINNING games you have played thus far.
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        },
        "played": 0,  # Total number of games you have played (WIN or LOSE or FORFEIT)
        "win_rate": 0,  # How many games did you win out of the total number of games you played, as a percentage
        "current_streak": 0,  # How many games have you WON successfully in a row.
        "max_streak": 0,  # Longest current streak you have had ever since you started playing Wordle
    }

    """ GET TOTAL PLAYED """
    games = request.user.games.all().order_by("-created_at")
    stat_context["played"] = games.count()

    # No game history
    if stat_context["played"] == 0:
        messages.add_message(request, messages.ERROR, "'No game stats'")
        return redirect("wordle_app:homepage")

    """ GET WIN RATE """
    won = games.filter(won=True)
    stat_context["win_rate"] = (won.count() / stat_context["played"]) * 100

    """ GET DISTRIBUTION """
    # https://stackoverflow.com/questions/37205793/django-values-list-vs-values
    tries = list(won.values_list("tries", flat=True))
    max_value = 0
    for k in stat_context["distribution"]:
        stat_context["distribution"][k] = tries.count(k)
    max_value = max(stat_context["distribution"].values())

    streaks = list(won.values_list("created_at", flat=True))

    # Have not won a game, current streak is 0
    if len(streaks) == 0:
        stat_context["current_streak"] = 0
    elif (
        is_same_date(games[0].created_at, timezone.localdate()) and games[0].won == False
    ):
        stat_context["current_streak"] = 0
    else:
        for i, streak in enumerate(streaks):
            if i == 0:
                if (timezone.localtime() - streak).days > 1:
                    break
                else:
                    stat_context["current_streak"] += 1

            elif ((streaks[i - 1]).day - streak.day) == 1:
                stat_context["current_streak"] += 1

            else:
                break

    # Have not won a game, max streak is 0
    if len(streaks) == 0:
        stat_context["max_streak"] = 0
    else:
        runner = 0
        max_count = 0

        for i, el in enumerate(streaks):
            if i == 0:
                runner += 1
            elif (streaks[i - 1].day - el.day) == 1:
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
