# Generated by Django 2.2.4 on 2019-10-09 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0021_auto_20191009_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='judgment',
        ),
        migrations.AddField(
            model_name='workflow',
            name='judgment_enough_information',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workflow',
            name='judgment_misleading_item',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workflow',
            name='judgment_remove_reduce_inform_head',
            field=models.TextField(blank=True, null=True),
        ),
    ]
