# Generated by Django 2.2.4 on 2019-10-03 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0019_auto_20191003_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
