# Generated by Django 4.2.4 on 2023-11-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('origin', models.CharField(max_length=70)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('is_magical', models.BooleanField(default=False)),
            ],
        ),
    ]
