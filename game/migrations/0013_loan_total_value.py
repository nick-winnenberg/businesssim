# Generated by Django 4.1.4 on 2023-07-25 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_report_average_meal_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='total_value',
            field=models.FloatField(default=0),
        ),
    ]
