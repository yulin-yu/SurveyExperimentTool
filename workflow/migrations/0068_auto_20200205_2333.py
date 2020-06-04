# Generated by Django 2.2.10 on 2020-02-05 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0067_auto_20200205_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_additional_information',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_inform',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, platforms should inform users that the item may be misleading.'), (False, 'No, platforms should not inform users that the item may be misleading.')], default=None, null=True, verbose_name='3. <b>Inform</b> users that the item may be misleading, if it is not removed.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_misleading_item',
            field=models.CharField(blank=True, choices=[('1', '1 = not misleading at all'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7 = false or extremely misleading')], default=None, max_length=1, null=True, verbose_name='Taking into account any evidence you found, how misleading is this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_reduce',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, platforms should reduce exposure to the item.'), (False, 'No, platforms should not reduce exposure to the item.')], default=None, null=True, verbose_name='2. <b>Reduce</b> the item’s audience, if it is not removed.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_remove',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, platforms should remove the item.'), (False, 'No, platforms should not remove the item.')], default=None, null=True, verbose_name='1. <b>Remove</b> the item.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='misinformation_harm',
            field=models.PositiveIntegerField(blank=True, choices=[(1, '1 = No harm at all'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7 = Extremely harmful')], default=None, null=True, verbose_name='How much harm would there be if people were misinformed about the topic of this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_a',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_any',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_b',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_c',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, one or more of these actions should be taken.'), (False, 'No, none of these actions should be taken.')], default=None, null=True, verbose_name='Based on your answers to the last two questions (misinformation and harm), in your personal opinion do you think that social media platforms and search engines should take <b>any of the following actions</b> on this item?\n                    <br></br>\n                    <ul>\n                    <li><b>Remove</b> the item.  <br>For example, Google would not present this item in search results. Facebook and Twitter would not present posts that link to this item anywhere.</li>\n                    <li><b>Reduce</b> the item’s audience, if it is not removed.  <br>For example, Google would present the item on the second page of search results, and Facebook and Twitter would present it where people have to scroll more before they see it. That way, fewer people would see it, but some people still would.</li>                    \n                    <li><b>Inform</b> users that the item may be misleading, if it is not removed.  <br>For example, there might be a “misleading” icon next to the item that users could click on to find out more information about it.</li>                    \n                    </ul>'),
        ),
    ]
