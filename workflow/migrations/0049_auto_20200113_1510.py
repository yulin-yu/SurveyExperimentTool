# Generated by Django 2.2.4 on 2020-01-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0048_merge_20200110_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mturk_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='rater',
            name='qualification',
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='ecoid',
            field=models.CharField(choices=[('1', 'Very Liberal'), ('2', 'Liberal'), ('3', 'Somewhat Liberal'), ('4', 'Moderate or Middle of the Road'), ('5', 'Somewhat Conservative'), ('6', 'Conservative'), ('7', 'Very Conservative')], default=False, max_length=5, verbose_name='Now when thinking about economic issues, how would you describe your political views?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polaf',
            field=models.CharField(choices=[('1', 'A Strong Democrat'), ('2', 'A Not Very Strong Democrat'), ('3', 'Independent, lean toward Democrat'), ('4', 'Independent (close to neither party)'), ('5', 'Independent, lean toward Republican'), ('6', 'A Not Very Strong Republican'), ('7', 'Strong Republican')], default=False, max_length=5, verbose_name='Generally speaking, when it comes to political parties in the United States, how would you best describe yourself?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polid',
            field=models.CharField(choices=[('1', 'Very Liberal'), ('2', 'Liberal'), ('3', 'Somewhat Liberal'), ('4', 'Moderate or Middle of the Road'), ('5', 'Somewhat Conservative'), ('6', 'Conservative'), ('7', 'Very Conservative')], default=False, max_length=5, verbose_name='Now when thinking about politics, how would you describe your political views?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='socid',
            field=models.CharField(choices=[('1', 'Very Liberal'), ('2', 'Liberal'), ('3', 'Somewhat Liberal'), ('4', 'Moderate or Middle of the Road'), ('5', 'Somewhat Conservative'), ('6', 'Conservative'), ('7', 'Very Conservative')], default=False, max_length=5, verbose_name='Now when thinking about social issues, how would you describe your political views?'),
        ),
    ]