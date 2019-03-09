# Generated by Django 2.1.2 on 2019-03-09 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datafetch', '0002_auto_20190309_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafetchsettings',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_settings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
