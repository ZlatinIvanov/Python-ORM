# Generated by Django 4.2.4 on 2023-11-20 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_order_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='main_app.product'),
        ),
    ]
