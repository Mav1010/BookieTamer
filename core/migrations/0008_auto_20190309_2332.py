# Generated by Django 2.1.2 on 2019-03-09 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190309_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='fortuna_url',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
