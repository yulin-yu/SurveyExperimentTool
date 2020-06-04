# Generated by Django 2.2.4 on 2020-02-01 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0056_auto_20200201_0128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workflow',
            old_name='judgment_item_matters',
            new_name='misinformation_harm',
        ),
        migrations.RemoveField(
            model_name='labelinganswer',
            name='judgment_item_matters',
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_inform',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should inform users that the item may be misleading.'), (False, 'No, platforms should not inform users that the item may be misleading.')], default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_misleading_item',
            field=models.CharField(choices=[('1', '1 = not misleading at all'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7 = false or extremely misleading')], default=None, max_length=1),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_reduce',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should reduce exposure to the item.'), (False, 'No, platforms should not reduce exposure to the item.')], default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_remove',
            field=models.BooleanField(choices=[(True, 'Yes, platforms should remove the item.'), (False, 'No, platforms should not remove the item.')], default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='misinformation_harm',
            field=models.PositiveIntegerField(choices=[('1', '1 = No harm at all'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7 = Extremely harmful')], default=None, verbose_name='How much harm would there be if people were misinformed about the topic of this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_a',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_b',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='predict_c',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None),
        ),
    ]
