# Generated by Django 2.2.4 on 2019-09-03 09:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('workflow', '0007_workflow_corroborating_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='type',
            field=models.CharField(choices=[
                ('without evidence url workflow', 'without evidence url workflow'),
                ('evidence url input workflow', 'evidence url input workflow'),
                ('evidence urls judgment workflow', 'evidence url input workflow')],
                default='without evidence url workflow', max_length=255),
        ),
    ]
