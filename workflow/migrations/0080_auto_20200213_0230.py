# Generated by Django 2.2.10 on 2020-02-13 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0079_auto_20200212_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labelinganswer',
            name='predict_any',
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None, verbose_name='Do you think you have enough information about the item to judge whether it is misleading?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_inform',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, if the item is not removed, platforms should inform users that it may be misleading.'), (False, 'No, platforms should not inform users that the item may be misleading.')], default=None, null=True, verbose_name='1. <b>Inform</b> users that the item may be misleading. (Assuming it is not removed.)'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_remove',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, platforms should remove the item.'), (False, 'No, platforms should not remove the item.')], default=None, null=True, verbose_name='3. <b>Remove</b> the item.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, one or more of these actions should be taken.'), (False, 'No, none of these actions should be taken.')], default=None, null=True, verbose_name='\n            \n            <br>There are three possible actions.</br>\n            <ul>\n                <li><b>Inform users</b>.\n                    <br><i>Show a "misleading" icon next to the item.</i></br>\n                </li>\n                <li><b>Reduce</b> the item’s audience.\n                    <br><i>Show the item on the second page of Google search results, and lower in Facebook and Twitter feeds.</i></br>\n                </li>\n                <li><b>Remove</b> the item. \n                    <br><i>Don’t show the item at all in Google search results or Facebook and Twitter feeds.</i></br>\n                </li>\n            </ul>\n            Based on your answers to the last two questions \n            (misinformation and harm), in your personal opinion do you think \n            that social media platforms and search engines should take \n            <b>at least one of these actions</b> on this item?\n        '),
        ),
    ]
