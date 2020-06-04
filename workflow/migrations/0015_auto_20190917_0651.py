# Generated by Django 2.2.4 on 2019-09-17 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0014_item_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
