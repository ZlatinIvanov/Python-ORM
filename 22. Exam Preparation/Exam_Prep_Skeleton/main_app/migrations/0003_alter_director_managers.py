# Generated by Django 4.2.4 on 2023-11-17 15:20

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_movie_director'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='director',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]