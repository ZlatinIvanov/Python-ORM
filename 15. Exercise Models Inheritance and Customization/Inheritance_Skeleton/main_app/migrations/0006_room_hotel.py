# Generated by Django 4.2.4 on 2023-11-15 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_hotel_room_specialreservation_regularreservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.hotel'),
            preserve_default=False,
        ),
    ]