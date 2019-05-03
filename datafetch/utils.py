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

    games_to_book = {'Match Day': [],
                     'Teams': [],
                     'Betting reason': [],
                     'X coef': [],
                     }

    for setting in fetch_settings:
        name = setting.name
        difference_x_range_min = setting.difference_x_range_min
        difference_x_range_max = setting.difference_x_range_max
        odds_1_min = setting.odds_1_min
        odds_1_max = setting.odds_1_max
        date_offset = setting.date_offset
        odds_2_min = setting.odds_2_min
        odds_2_max = setting.odds_2_max

        leagues = setting.leagues

        date_limit = datetime.today() + timedelta(setting.date_offset)

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

                    if difference_x_range_max and difference_x_range_min:
                        if (difference_x_range_min <= difference <= difference_x_range_max):
                            games_to_book['Match Day'].append(match_day)
                            games_to_book['Teams'].append('{} - {}'.format(teams.split(" ")[0], teams.split(" ")[2]))
                            games_to_book['Betting reason'].append(difference)
                            games_to_book['X coef'].append(coef_x)
                    if odds_1_min and odds_1_max:
                        if (odds_1_min <= coef_1 <= odds_1_max):
                            games_to_book['Match Day'].append(match_day)
                            games_to_book['Teams'].append(teams[:-3])
                            games_to_book['Betting reason'].append(coef_1)
                            games_to_book['X coef'].append("-")
                    if odds_2_min and odds_2_max:
                        if (odds_2_min <= coef_2 <= odds_2_max):
                            games_to_book['Match Day'].append(match_day)
                            games_to_book['Teams'].append(teams[:-3])
                            games_to_book['Betting reason'].append(coef_2)
                            games_to_book['X coef'].append("-")

    return pd.DataFrame(games_to_book)