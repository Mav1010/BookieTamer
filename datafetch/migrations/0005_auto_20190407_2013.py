# Generated by Django 2.1.2 on 2019-04-07 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datafetch', '0004_datafetchsettings_leagues'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafetchsettings',
            name='odds_1_max_second',
        ),
        migrations.RemoveField(
            model_name='datafetchsettings',
            name='odds_1_min_second',
        ),
        migrations.AddField(
            model_name='datafetchsettings',
            name='name',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='datafetchsettings',
            name='odds_2_max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datafetchsettings',
            name='odds_2_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datafetchsettings',
            name='difference_x_range_max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datafetchsettings',
            name='difference_x_range_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datafetchsettings',
            name='odds_1_max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datafetchsettings',
            name='odds_1_min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datafetchsettings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_settings', to=settings.AUTH_USER_MODEL),
        ),
    ]
