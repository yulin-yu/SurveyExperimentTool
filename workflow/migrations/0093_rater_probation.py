# Generated by Django 2.2.10 on 2020-02-20 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0092_auto_20200219_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='rater',
            name='probation',
            field=models.BooleanField(default=False),
        ),
    ]
