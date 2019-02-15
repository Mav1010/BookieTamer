import pandas as pd

from datetime import timedelta, date, datetime
import BookieTamer.settings as settings

from datafetch.models import DataFetchSettings

def bookie_probability_real(x1, xX, x2):

    bookie_rate_1 = x1
    bookie_rate_X = xX
    bookie_rate_2 = x2

    bookie_probabilty_normal = (1 / bookie_rate_1) + (1 / bookie_rate_X) + (1 / bookie_rate_2)

    context = {
        'bookie_probabilty_normal': bookie_probabilty_normal,
        'bookie_probabilty_real_1': round((1 / bookie_rate_1) / bookie_probabilty_normal, 3),
        'bookie_probabilty_real_2': round((1 / bookie_rate_2) / bookie_probabilty_normal, 3),
        'bookie_probabilty_real_X': round((1 / bookie_rate_X) / bookie_probabilty_normal, 3),
    }

    return context

def get_fortuna_games():

    all_leagues = [settings.FORTUNA_URL_SERIE_A, settings.FORTUNA_URL_PREMIER_LEAGUE, settings.FORTUNA_URL_LIGUE_1,
                   settings.FORTUNA_URL_PRIMERA_DIVISION, settings.FORTUNA_URL_BUNDESLIGA]

    current_year = date.today().year

    datafetch_settings = DataFetchSettings.objects.get(pk=1)

    difference_x_range_min = datafetch_settings.difference_x_range_min
    difference_x_range_max = datafetch_settings.difference_x_range_max
    odds_1_min = datafetch_settings.odds_1_min
    odds_1_max = datafetch_settings.odds_1_max
    date_offset = datafetch_settings.date_offset
    odds_1_min_second = datafetch_settings.odds_1_min_second
    odds_1_max_second = datafetch_settings.odds_1_max_second

    date_limit = datetime.today() + timedelta(date_offset)

    games_to_book = {'Match Day': [],
                     'Teams': [],
                     'Betting reason': [],
                     'X coef': [],
                     }

    for league in all_leagues:
        current_games = pd.read_html(settings.BASE_FORTUNA_URL + league)[2]
        try:
            games = pd.DataFrame(current_games[['zápas', '1', '0', '2', 'datum']])
        except KeyError:
            continue
        #renaming columns for easier use
        games.columns = ['games', 'x1', 'xX', 'x2', 'date']

        for index, row in games.iterrows():
            #check if row has empty values
            if not row.isnull().any():
                #convert string to date object
                try:
                    match_day = datetime.strptime(row.date.split(" ")[0] + str(current_year), '%d.%m.%Y')
                except ValueError:
                    match_day = None
                    continue
            else:
                match_day = None

            if (not row.isnull().any()) and (match_day <= date_limit):
                teams = row['games']
                coef_1 = float(row['x1'])
                coef_x = float(row['xX'])
                coef_2 = float(row['x2'])

                #gets real bookmakers probabilities
                coef_probability = bookie_probability_real(coef_1, coef_x, coef_2)
                difference = round(
                    (coef_probability['bookie_probabilty_real_1']) - (coef_probability['bookie_probabilty_real_2']), 3)

                if (difference_x_range_min <= difference <= difference_x_range_max):
                    games_to_book['Match Day'].append(match_day)
                    games_to_book['Teams'].append('{} - {}'.format(teams.split(" ")[0], teams.split(" ")[2]))
                    games_to_book['Betting reason'].append(difference)
                    games_to_book['X coef'].append(coef_x)
                if (odds_1_min <= coef_1 <= odds_1_max):
                    games_to_book['Match Day'].append(match_day)
                    games_to_book['Teams'].append(teams[:-3])
                    games_to_book['Betting reason'].append(coef_1)
                    games_to_book['X coef'].append("-")
                if (odds_1_min_second <= coef_1 <= odds_1_max_second):
                    games_to_book['Match Day'].append(match_day)
                    games_to_book['Teams'].append(teams[:-3])
                    games_to_book['Betting reason'].append(coef_1)
                    games_to_book['X coef'].append("-")

    return pd.DataFrame(games_to_book)