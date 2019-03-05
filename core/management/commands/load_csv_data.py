import csv
import logging

from django.conf import settings
from django.core.management import BaseCommand
from core.models import Match, Team, Division


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates model with csv data'

    def handle(self, *args, **kwargs):

        errors = []
        all_games = Match.objects.all()
        #import teams
        with open(settings.MATCH_HISTORY_DATA_PATH + 'full_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # game_id = row['game_id']
                # if not all_games.filter(game_id=game_id).exists():

                home_team = row['home_team']
                away_team = row['away_team']

                try:
                    division = Division.objects.get(name=row['league'])
                except Division.DoesNotExist:
                    division = Division.objects.create(name=row['league'])

                if not Team.objects.filter(name=home_team).exists():
                    team_instance = Team.objects.create(name=home_team, division=division)
                    team_instance.save()
                if not Team.objects.filter(name=away_team).exists():
                    team_instance = Team.objects.create(name=away_team, division=division)
                    team_instance.save()

                #import games
                # logger.warning("this is row {}".format(row['game_id']))
                division = division
                date = row['date']
                home_team = Team.objects.get(name=row['home_team'])
                away_team = Team.objects.get(name=row['away_team'])

                try:
                    ft_home_goals = int(row['FTHG'].split('.')[0])
                except ValueError:
                    continue

                try:
                    ft_away_goals = int(row['FTAG'].split('.')[0])
                except ValueError:
                    continue
                ft_result = row['FTR']

                try:
                    ht_home_goals = int(row['HTHG'].split('.')[0])
                except ValueError:
                    continue

                try:
                    ht_away_goals = int(row['HTAG'].split('.')[0])
                except ValueError:
                    continue

                ht_result = row['HTR']
                odds_home = row['PSH']
                odds_draw = row['PSD']
                odds_away = row['PSA']

                try:
                    new_match = Match(division=division, date=date, home_team=home_team, away_team=away_team, ft_home_goals=ft_home_goals, ft_away_goals=ft_away_goals, ft_result=ft_result,
                    ht_home_goals=ht_home_goals, ht_away_goals=ht_away_goals, ht_result=ht_result, odds_home=odds_home, odds_draw=odds_draw, odds_away=odds_away)
                    new_match.save()
                except ValueError:
                    # errors.append(row['game_id'])
                    print(errors)
                    print(len(errors))

            f.close()
            