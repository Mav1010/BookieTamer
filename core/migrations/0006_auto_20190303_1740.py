# Generated by Django 2.1.2 on 2019-03-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20181028_1135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['-date'], 'verbose_name_plural': 'matches'},
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(choices=[('ITA-Serie A', 'Serie A'), ('ENG-Premier League', 'Premier League'), ('GER-Bundesliga', 'Bundesliga'), ('FRA-Ligue 1', 'Ligue 1'), ('ESP-La Liga', 'Primera Division')], max_length=50),
        ),
        migrations.AlterField(
            model_name='match',
            name='ft_result',
            field=models.CharField(choices=[('H', 'H'), ('D', 'X'), ('A', 'A')], max_length=1),
        ),
        migrations.AlterField(
            model_name='match',
            name='ht_result',
            field=models.CharField(choices=[('H', 'H'), ('D', 'X'), ('A', 'A')], max_length=1),
        ),
    ]
