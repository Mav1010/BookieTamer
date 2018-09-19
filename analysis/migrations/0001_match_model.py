# Generated by Django 2.0.2 on 2018-09-18 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.IntegerField(null=True)),
                ('date', models.DateField(null=True)),
                ('home_team', models.TextField(max_length=50)),
                ('away_team', models.TextField(max_length=50)),
                ('ft_home_goals', models.SmallIntegerField()),
                ('ft_away_goals', models.SmallIntegerField()),
                ('ft_result', models.SmallIntegerField()),
                ('ht_home_goals', models.SmallIntegerField()),
                ('ht_away_goals', models.SmallIntegerField()),
                ('ht_result', models.SmallIntegerField()),
                ('odds_home', models.FloatField()),
                ('odds_draw', models.FloatField()),
                ('odds_away', models.FloatField()),
            ],
        ),
    ]
