import pdb
from django.http import HttpResponse
from django.shortcuts import render

from wordle_app.models import Game

# Create your views here.


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

    player = Game.objects.filter(player__exact=request.user.id)
    stat_context["played"] = player.count()

    won = player.filter(won=True)
    stat_context["win_rate"] = won.count() / stat_context["played"]

    # https://stackoverflow.com/questions/37205793/django-values-list-vs-values
    wins = list(won.values_list("tries", flat=True))
    for k in stat_context["distribution"]:
        stat_context["distribution"][k] = wins.count(k)

    return render(request, "wordle_stat/index.html", {"stat": stat_context})
