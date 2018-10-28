from django.shortcuts import render_to_response

from datafetch.utils import get_fortuna_games

def games_to_bet_list(request):

    df = get_fortuna_games()
    html_table = df.to_html(index=False)

    return render_to_response('datafetch/games_to_bet.html', {'html_table': html_table})