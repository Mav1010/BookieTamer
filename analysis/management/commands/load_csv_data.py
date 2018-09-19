import csv
import logging
from django.core.management import BaseCommand
from analysis.models import Match


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates model with csv data'

    def handle(self, *args, **kwargs):
        with open('C:\\Users\\Mac\\PycharmProjects\\BookieTamer\\data1.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logger.warning("this is row {}".format(row['odds_home']))
                division=row['division']
                date=row['date']
                home_team=row['home_team']
                away_team=row['away_team']
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
            