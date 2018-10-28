import pandas as pd

from datetime import timedelta, date, datetime
import BookieTamer.settings as settings

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

    date_limit = datetime.today() + timedelta(settings.DATE_OFFSET)
    current_year = date.today().year

    games_to_book = {'Match Day': [],
                     'Teams': [],
                     'Betting reason': [],
                     'X coef': [],
                     }

    for league in all_leagues:
        current_games = pd.read_html(settings.BASE_FORTUNA_URL + league)[2]
        games = pd.DataFrame(current_games[['zápas', '1', '0', '2', 'datum']])
        #renaming columns for easier use
        games.columns = ['games', 'x1', 'xX', 'x2', 'date']

        for index, row in games.iterrows():
            #check if row has empty values
            if not row.isnull().any():
                #check if date is 1-9, or 10-31, then coverts it to datetime object
                if len(row.date) == 12:
                    match_day = datetime.strptime(row.date[:5] + '.' + str(current_year), '%d.%m.%Y')
                else:
                    match_day = datetime.strptime(row.date[:4] + '.' + str(current_year), '%d.%m.%Y')
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

                if (settings.DIFFERENCE_RANGE_MIN_X <= difference <= settings.DIFFERENCE_RANGE_MAX_X):
                    games_to_book['Match Day'].append(match_day)
                    games_to_book['Teams'].append(teams[:-3])
                    games_to_book['Betting reason'].append(difference)
                    games_to_book['X coef'].append(coef_x)
                if (settings.RATE_1_MIN <= coef_1 <= settings.RATE_1_MAX):
                    games_to_book['Match Day'].append(match_day)
                    games_to_book['Teams'].append(teams[:-3])
                    games_to_book['Betting reason'].append(coef_1)
                    games_to_book['X coef'].append("-")

    return pd.DataFrame(games_to_book)