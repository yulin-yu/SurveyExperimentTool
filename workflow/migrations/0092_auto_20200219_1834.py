# Generated by Django 2.2.10 on 2020-02-19 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0091_auto_20200219_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemworkflow',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='rater',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]