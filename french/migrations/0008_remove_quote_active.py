# Generated by Django 4.0.5 on 2022-07-24 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('french', '0007_alter_quote_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='active',
        ),
    ]
