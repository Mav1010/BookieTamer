import pandas as pd

from datetime import timedelta, date, datetime
import BookieTamer.settings as settings


def bookie_probability_real(x1, xX, x2):
    try:
        bookie_probability_normal = (1 / x1) + (1 / xX) + (1 / x2)
    except (ZeroDivisionError, TypeError):
        bookie_probability_normal = 1

    try:
        bookie_probability_real_1 = round((1 / x1) / bookie_probability_normal, 3)
    except (ZeroDivisionError, TypeError):
        bookie_probability_real_1 = 1

    try:
        bookie_probability_real_2 = round((1 / x2) / bookie_probability_normal, 3)
    except (ZeroDivisionError, TypeError):
        bookie_probability_real_2 = 1

    try:
        bookie_probability_real_x = round((1 / xX) / bookie_probability_normal, 3)
    except (ZeroDivisionError, TypeError):
        bookie_probability_real_x = 1

    context = {
        'bookie_probability_normal': bookie_probability_normal,
        'bookie_probability_real_1': bookie_probability_real_1,
        'bookie_probability_real_2': bookie_probability_real_2,
        'bookie_probability_real_x': bookie_probability_real_x,
    }
    return context


def get_fortuna_games(fetch_settings):
    current_year = date.today().year

    to_bet = pd.DataFrame()

    for setting in fetch_settings:
        name = setting.name
        max_difference_x_probability = setting.max_difference_x_probability
        odds_1_min_probability = setting.odds_1_min_probability
        odds_1_max_probability = setting.odds_1_max_probability
        date_offset = setting.date_offset
        odds_2_min_probability = setting.odds_2_min_probability
        odds_2_max_probability = setting.odds_2_max_probability

        leagues = setting.leagues

        date_limit = datetime.today() + timedelta(setting.date_offset)

        for league in leagues.all():
            current_games = pd.read_html(settings.BASE_FORTUNA_URL + league.fortuna_url)[0]
            try:
                # get columns of the dataframe by the location of columns,
                # instead of using names (like Zapas, datum etc.)
                games = current_games[['Zápas sázka na výsledek zápasu', '1', '0', '2', 'datum']]
            except KeyError:
                continue
            # renaming columns for easier use
            games.columns = ['games', 'x1', 'xX', 'x2', 'date']
            games.loc[:, 'games'] = games['games'].apply(lambda x: x.split("  ")[0])

            games.loc[:, 'date'] = games['date'].apply(lambda x: convert_date_to_datetime(x, current_year))
            games = games[games['date'] <= date_limit]  # get the games within the date limit

            # remove games that are null values in any of the columns (e.g. the game is already underway)
            games = games.dropna()
            probabilities = bookie_probability_real(games.x1, games.xX, games.x2)

            games['b_prob_normal'] = round(probabilities.get('bookie_probability_normal'), 3)
            games['b_prob_1'] = probabilities.get('bookie_probability_real_1')
            games['b_prob_X'] = probabilities.get('bookie_probability_real_x')
            games['b_prob_2'] = probabilities.get('bookie_probability_real_2')
            games['prob12_difference'] = round(games.b_prob_1 - games.b_prob_2, 3)

            games['bet_X'] = games['prob12_difference'] <= max_difference_x_probability
            games['bet_1'] = ((odds_1_min_probability <= games['b_prob_1']) & (games['b_prob_1'] <= odds_1_max_probability))
            games['bet_2'] = ((odds_2_min_probability <= games['b_prob_2']) & (games['b_prob_2'] <= odds_2_max_probability))

            to_bet = pd.concat([to_bet, games])

    return pd.DataFrame(to_bet)


def convert_date_to_datetime(match_date_str, current_year):
    if isinstance(match_date_str, str):
        match_date = match_date_str.split('\xa0')[0]
        match_date = datetime.strptime(match_date + str(current_year), '%d.%m.%Y')
        return match_date
