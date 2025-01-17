# Generated by Django 2.2.10 on 2020-02-17 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0085_auto_20200215_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labelinganswer',
            name='judgment',
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_misleading_item',
            field=models.PositiveIntegerField(blank=True, choices=[(None, ''), (1, '1 = not misleading at all'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7 = false or extremely misleading'), (0, "I don't have enough information to make a judgment")], default=None, null=True, verbose_name='How misleading is this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.CharField(choices=[('Yes', 'Yes, one or more of these actions should be taken.'), ('No', 'No, none of these actions should be taken.'), ('Not enough info', "I don't have enough information to judge")], default=None, max_length=32, verbose_name='\n            Based on your answers to the last two questions \n            (misinformation and harm), in your personal opinion do you think \n            that social media platforms and search engines should take \n            <b>at least one of these actions</b> on this item?\n        '),
        ),
    ]

