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
                     'coef': [],
                     }

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
            current_games = pd.read_html(settings.BASE_FORTUNA_URL + league.fortuna_url)[1]
            try:
                # get columns of the dataframe by the location of columns,
                # instead of using names (like Zapas, datum etc.)
                games = pd.DataFrame(current_games.iloc[:, [0, 1, 2, 3, 8]])
            except KeyError:
                continue
            # renaming columns for easier use
            games.columns = ['games', 'x1', 'xX', 'x2', 'date']

            for index, row in games.iterrows():
                # check if row has empty values
                if not row.isnull().any():
                    # convert string to date object
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

                    # gets real bookmakers probabilities
                    coef_probability = bookie_probability_real(coef_1, coef_x, coef_2)
                    difference = round(
                        (coef_probability['bookie_probabilty_real_1']) - (coef_probability['bookie_probabilty_real_2']), 3)

                    if difference and max_difference_x_probability:
                        if abs(difference) <= max_difference_x_probability:
                            games_to_book['Match Day'].append(match_day)
                            games_to_book['Teams'].append('{} - {}'.format(teams.split(" ")[0], teams.split(" ")[2]))
                            games_to_book['Betting reason'].append('Draw: {}'.format(difference))
                            games_to_book['coef'].append(coef_x)
                    if odds_1_min_probability and odds_1_max_probability:
                        if (odds_1_min_probability <= coef_probability['bookie_probabilty_real_1'] <= odds_1_max_probability):
                            games_to_book['Match Day'].append(match_day)
                            games_to_book['Teams'].append(teams[:-3])
                            games_to_book['Betting reason'].append('Home: {}'.format(coef_probability['bookie_probabilty_real_1']))
                            games_to_book['coef'].append(coef_1)
                    if odds_2_min_probability and odds_2_max_probability:
                        if (odds_2_min_probability <= coef_probability['bookie_probabilty_real_2'] <= odds_2_max_probability):
                            games_to_book['Match Day'].append(match_day)
                            games_to_book['Teams'].append(teams[:-3])
                            games_to_book['Betting reason'].append('Away: {}'.format(coef_probability['bookie_probabilty_real_1']))
                            games_to_book['coef'].append(coef_2)

    return pd.DataFrame(games_to_book)