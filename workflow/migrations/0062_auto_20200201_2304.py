# Generated by Django 2.2.4 on 2020-02-01 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0061_merge_20200201_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='labelinganswer',
            name='predict_any',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='evidence',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None, null=True, verbose_name='Were you able to find some other web page or video with corroborating or challenging evidence that you thought was convincing? If so, paste the URL that you found most informative and convincing. (Note: please paste the URL for a specific web page, not a search engine query.)'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_inform',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should inform users that the item may be misleading.'), (False, 'No, platforms should not inform users that the item may be misleading.')], default=None, verbose_name='3. <b>Inform</b> users that the item may be misleading, if it is not removed.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_reduce',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should reduce exposure to the item.'), (False, 'No, platforms should not reduce exposure to the item.')], default=None, verbose_name='2. <b>Reduce</b> the item’s audience, if it is not removed.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_remove',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should remove the item.'), (False, 'No, platforms should not remove the item.')], default=None, verbose_name='1. <b>Remove</b> the item.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.BooleanField(choices=[(True, 'Yes, one or more of these actions should be taken.'), (False, 'No, none of these actions should be taken.')], default=None, verbose_name='Based on your answers to the last two questions (misinformation and harm), in your personal opinion do you think that social media platforms and search engines should take <b>any of the following actions</b> on this item?\n                    <br></br>\n                    <ul>\n                    <li><b>Remove</b> the item.  <br>For example, Google would not present this item in search results. Facebook and Twitter would not present posts that link to this item anywhere.</li>\n                    <li><b>Reduce</b> the item’s audience, if it is not removed.  <br>For example, Google would present the item on the second page of search results, and Facebook and Twitter would present it where people have to scroll more before they see it. That way, fewer people would see it, but some people still would.</li>                    \n                    <li><b>Inform</b> users that the item may be misleading, if it is not removed.  <br>For example, there might be a “misleading” icon next to the item that users could click on to find out more information about it.</li>                    \n                    </ul>'),
        ),
    ]
