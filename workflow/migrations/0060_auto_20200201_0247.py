# Generated by Django 2.2.4 on 2020-02-01 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0059_auto_20200201_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None, verbose_name='Do you think you have enough information about the item to make a judgment about whether it is misleading?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_inform',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should inform users that the item may be misleading.'), (False, 'No, platforms should not inform users that the item may be misleading.')], default=None, verbose_name='Inform users that item may be misleading, if it is not removed. For example, there might be a “misleading” icon next to the item that users could click on to find out more information about it.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_misleading_item',
            field=models.CharField(choices=[('1', '1 = not misleading at all'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7 = false or extremely misleading')], default=None, max_length=1, verbose_name='Taking into account any evidence you found, how misleading is this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_reduce',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should reduce exposure to the item.'), (False, 'No, platforms should not reduce exposure to the item.')], default=None, verbose_name='Reduce the item’s audience, if it is not removed. For example, Google would present the item on the second page of search results, and Facebook and Twitter would present it where people have to scroll more before they see it. That way, fewer people would see it, but some people still would.'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_remove',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should remove the item.'), (False, 'No, platforms should not remove the item.')], default=None, verbose_name='Remove the item. For example, Google would not present this item in search results. Facebook and Twitter would not present posts that link to this item anywhere.'),
        ),
    ]
