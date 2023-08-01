# Generated by Django 4.1.4 on 2023-07-24 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_alter_report_final_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='average_meal_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='average_quantity_sold',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_comissions',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_event_payments',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_fixed_costs',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_ingredient_costs',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_loan_payments',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_marketing_spend',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_net_income',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_profit',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_revenue',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_salaries',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_sales',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_tax_payments',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='total_varriable_costs',
            field=models.FloatField(default=0),
        ),
    ]
