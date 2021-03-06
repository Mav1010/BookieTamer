# Generated by Django 2.1.2 on 2019-03-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190303_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='date_changed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='division',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2018-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='date_changed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='match',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2018-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='date_changed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='team',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2018-01-01'),
            preserve_default=False,
        ),
    ]
