# Generated by Django 2.2.10 on 2020-02-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0093_rater_probation'),
    ]

    operations = [
        migrations.AddField(
            model_name='corroboratingchoices',
            name='correct_for_workflows',
            field=models.ManyToManyField(to='workflow.Workflow'),
        ),
    ]
