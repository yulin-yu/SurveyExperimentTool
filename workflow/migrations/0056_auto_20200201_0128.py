# Generated by Django 2.2.4 on 2020-02-01 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0055_rater_rater_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='labelinganswer',
            name='judgment_item_matters',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], default=1, max_length=1),
        ),
        migrations.AddField(
            model_name='workflow',
            name='judgment_item_matters',
            field=models.TextField(blank=True, null=True),
        ),
    ]
