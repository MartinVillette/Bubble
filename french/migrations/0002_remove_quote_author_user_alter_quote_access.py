# Generated by Django 4.0.5 on 2022-07-23 10:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('french', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='author_user',
        ),
        migrations.AlterField(
            model_name='quote',
            name='access',
            field=models.ManyToManyField(related_name='access_user_french', to=settings.AUTH_USER_MODEL),
        ),
    ]
