import csv
import footballdata as fd
import pandas as pd
import os
import shutil

from django.conf import settings
from django.core.management import BaseCommand


leagues = ['ENG-Premier League', 'ESP-La Liga', 'FRA-Ligue 1', 'GER-Bundesliga', 'ITA-Serie A']
seasons = ['1314', '1415', '1516', '1617', '1718', '1819']
entry_path = settings.MATCH_HISTORY_DATA_PATH
all_files = ['{}.csv'.format(league) for league in leagues]

def put_files_together():
    all_files = ['{}.csv'.format(league) for league in leagues]
    header_saved = False
    with open('full_data.csv', 'w') as complete_file:
        writer = csv.writer(complete_file)
        for file in all_files:
            with open('{}{}'.format(entry_path, file)) as league_file:
                header = next(league_file)
                if not header_saved:    
                    complete_file.write(header)
                    header_saved = True
                for line in league_file:
                    complete_file.write(line)


def delete_temp_files():
    all_files = ['{}{}.csv'.format(entry_path, league) for league in leagues]
    for file in all_files:
        os.remove(file)
    shutil.rmtree('{}{}'.format(entry_path, 'data'), ignore_errors=True)


class Command(BaseCommand):
    help = 'Downloads data from football-data over the specified seasons and leagues'

    def handle(self, *args, **options):
        def get_match_history(league):
            history = fd.MatchHistory(league, seasons)
            for i in range(len(seasons)+1):
                try:
                    games = history.read_games()
                except FileExistsError:
                    pass
            games = history.read_games()

            games = pd.DataFrame(games)
            if 'Referee' in games.columns:
                games.drop('Referee', axis=1, inplace=True)
            games.to_csv('{}.csv'.format(league))

        for league in leagues:
            get_match_history(league)

        put_files_together()
        delete_temp_files()
