# Generated by Django 4.1.4 on 2023-07-12 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
