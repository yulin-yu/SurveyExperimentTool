# Generated by Django 2.2.10 on 2020-02-13 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0081_auto_20200213_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='inform_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='reduce_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='remove_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='total_simulated_answers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]