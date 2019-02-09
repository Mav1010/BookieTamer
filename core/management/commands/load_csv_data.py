import csv
import logging
from django.core.management import BaseCommand
from core.models import Match, Team, Division


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates model with csv data'

    def handle(self, *args, **kwargs):

        #import teams
        with open('C:\\Users\\Mac\\PycharmProjects\\BookieTamer\\data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                home_team = row['home_team']
                away_team = row['away_team']

                try:
                    division = Division.objects.get(name=row['division'])
                except Division.DoesNotExist:
                    division = Division.objects.create(name=row['division'])

                if not Team.objects.filter(name=home_team).exists():
                    team_instance = Team.objects.create(name=home_team, division=division)
                    team_instance.save()
                if not Team.objects.filter(name=away_team).exists():
                    team_instance = Team.objects.create(name=away_team, division=division)
                    team_instance.save()

                #import games
                logger.warning("this is row {}".format(row['odds_home']))
                division=division
                date=row['date']
                home_team=Team.objects.get(name=row['home_team'])
                away_team=Team.objects.get(name=row['away_team'])
                ft_home_goals=row['ft_home_goals']
                ft_away_goals=row['ft_away_goals']
                ft_result=row['ft_result']
                ht_home_goals=row['ht_home_goals']
                ht_away_goals=row['ht_away_goals']
                ht_result=row['ht_result']
                odds_home=row['odds_home']
                odds_draw=row['odds_draw']
                odds_away=row['odds_away']
                new_match = Match(division=division, date=date, home_team=home_team, away_team=away_team, ft_home_goals=ft_home_goals, ft_away_goals=ft_away_goals, ft_result=ft_result, 
                ht_home_goals=ht_home_goals, ht_away_goals=ht_away_goals, ht_result=ht_result, odds_home=odds_home, odds_draw=odds_draw, odds_away=odds_away)
                new_match.save()
                f.close
            