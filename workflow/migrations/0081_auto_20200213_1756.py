# Generated by Django 2.2.10 on 2020-02-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0080_auto_20200213_0230'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WarnPeopleChoices',
            new_name='InformChoices',
        ),
        migrations.RenameModel(
            old_name='ReduceNumberOfPeopleChoices',
            new_name='ReduceChoices',
        ),
    ]