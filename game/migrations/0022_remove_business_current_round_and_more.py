# Generated by Django 4.1.4 on 2023-08-15 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_alter_business_yearsprofessionalexperince_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='current_round',
        ),
        migrations.AddField(
            model_name='business',
            name='decision_making',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='endurance',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='identity_development',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='influence',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='market_awareness',
            field=models.FloatField(default=0, null=True),
        ),
    ]
