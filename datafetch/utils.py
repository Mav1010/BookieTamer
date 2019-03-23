import pandas as pd

from datetime import timedelta, date, datetime
import BookieTamer.settings as settings


def bookie_probability_real(x1, xX, x2):
    bookie_probabilty_normal = (1 / x1) + (1 / xX) + (1 / x2)

    context = {
        'bookie_probabilty_normal': bookie_probabilty_normal,
        'bookie_probabilty_real_1': round((1 / x1) / bookie_probabilty_normal, 3),
        'bookie_probabilty_real_2': round((1 / x2) / bookie_probabilty_normal, 3),
        'bookie_probabilty_real_X': round((1 / xX) / bookie_probabilty_normal, 3),
    }
    return context


def get_fortuna_games(fetch_settings):
    current_year = date.today().year

    difference_x_range_min = fetch_settings.difference_x_range_min
    difference_x_range_max = fetch_settings.difference_x_range_max
    odds_1_min = fetch_settings.odds_1_min
    odds_1_max = fetch_settings.odds_1_max
    date_offset = fetch_settings.date_offset
    odds_1_min_second = fetch_settings.odds_1_min_second
    odds_1_max_second = fetch_settings.odds_1_max_second

    leagues = fetch_settings.leagues

    date_limit = datetime.today() + timedelta(date_offset)

    games_to_book = {'Match Day': [],
                     'Teams': [],
                     'Betting reason': [],
                     'X coef': [],
                     }

    for league in leagues.all():
        current_games = pd.read_html(settings.BASE_FORTUNA_URL + league.fortuna_url)[1]
        try:
            #get columns of the dataframe by the location of columns, instead of using names (like Zapas, datum etc.)
            games = pd.DataFrame(current_games.iloc[:, [0, 1, 2, 3, 8]]) 
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