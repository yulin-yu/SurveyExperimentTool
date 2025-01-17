# Generated by Django 2.2.4 on 2020-02-01 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0058_workflow_take_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None, verbose_name='Based on your answers to the last two questions (misinformation and harm), in your personal opinion do you think that social media platforms and search engines should take any action on this item?'),
        ),
    ]
