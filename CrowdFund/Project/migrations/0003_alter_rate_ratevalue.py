# Generated by Django 5.0.3 on 2024-03-28 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rateValue',
            field=models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]
