# Generated by Django 4.1 on 2022-08-25 16:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0017_alter_englishlesson_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishlesson',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 25, 16, 0, 50, 825508), editable=False),
        ),
    ]
