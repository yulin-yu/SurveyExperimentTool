# Generated by Django 2.2.10 on 2020-02-10 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0072_auto_20200210_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='labelinganswer',
            name='corroborating_link_clicked',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='labelinganswer',
            name='item_link_clicked',
            field=models.NullBooleanField(),
        ),
    ]