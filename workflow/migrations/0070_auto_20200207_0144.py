# Generated by Django 2.2.10 on 2020-02-07 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0069_auto_20200205_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographicsanswer',
            name='gender_other',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Self-described gender'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='age',
            field=models.CharField(choices=[(None, ''), ('< 18', 'Under 18 years old'), ('18-29', '18-29 years old'), ('30-39', '30-39 years old'), ('40-49', '40-49 years old'), ('50-59', '50-59 years old'), ('> 60', '60 years or older')], default=False, max_length=5, null=True, verbose_name='What is your age?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='education',
            field=models.CharField(choices=[(None, ''), ('1', 'Less than high school degree'), ('2', 'High school degree or equivalent (e.g., GED)'), ('3', 'Some college but no degree'), ('4', 'Associate degree'), ('5', 'Bachelor degree'), ('6', 'Graduate degree')], default=False, max_length=5, null=True, verbose_name='What is the highest level of school you have completed or the highest degree you have received?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='gender',
            field=models.CharField(choices=[(None, ''), ('f', 'Female'), ('m', 'Male'), ('3', 'Non-binary / third gender'), ('_', 'Prefer to self-describe'), ('x', 'Prefer not to say')], default=False, max_length=5, null=True, verbose_name='What is your gender?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polaf',
            field=models.CharField(choices=[(None, ''), ('1', 'A Strong Democrat'), ('2', 'A Not Very Strong Democrat'), ('3', 'Independent, lean toward Democrat'), ('4', 'Independent (close to neither party)'), ('5', 'Independent, lean toward Republican'), ('6', 'A Not Very Strong Republican'), ('7', 'Strong Republican'), ('_', 'Something else, please specify')], default=False, max_length=5, null=True, verbose_name='Generally speaking, when it comes to political parties in the United States, how would you best describe yourself?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polaf_other',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Specify something else'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polid',
            field=models.CharField(choices=[(None, ''), ('1', 'Very Liberal'), ('2', 'Liberal'), ('3', 'Somewhat Liberal'), ('4', 'Moderate or Middle of the Road'), ('5', 'Somewhat Conservative'), ('6', 'Conservative'), ('7', 'Very Conservative'), ('_', 'Something else, please specify')], max_length=5, null=True, verbose_name='Now when thinking about politics, how would you describe your political views?'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polid_other',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Specify something else'),
        ),
        migrations.AlterField(
            model_name='demographicsanswer',
            name='polint',
            field=models.CharField(choices=[(None, ''), ('1', 'most of the time'), ('2', 'some of the time'), ('3', 'only now and then'), ('4', 'hardly at all')], default=False, max_length=5, verbose_name='Would you say you follow what’s going on in government and public affairs:'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='judgment_misleading_item',
            field=models.PositiveIntegerField(blank=True, choices=[(None, ''), (1, '1 = not misleading at all'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7 = false or extremely misleading')], default=None, null=True, verbose_name='Taking into account any evidence you found, how misleading is this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='misinformation_harm',
            field=models.PositiveIntegerField(blank=True, choices=[(None, ''), (1, '1 = No harm at all'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7 = Extremely harmful')], default=None, null=True, verbose_name='How much harm would there be if people were misinformed about the topic of this item?'),
        ),
        migrations.AlterField(
            model_name='labelinganswer',
            name='take_action',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes, one or more of these actions should be taken.'), (False, 'No, none of these actions should be taken.')], default=None, null=True, verbose_name='\n            Based on your answers to the last two questions \n            (misinformation and harm), in your personal opinion do you think \n            that social media platforms and search engines should take \n            <b>any of the following actions</b> on this item?\n            <br></br>\n            <ul>\n                <li><b>Remove</b> the item.  \n                    <br>For example, Google would not present this item in \n                    search results. Facebook and Twitter would not present \n                    posts that link to this item anywhere.</li>\n                <li><b>Reduce</b> the item’s audience, \n                    if it is not removed.  \n                    <br>For example, Google would present the item on the \n                    second page of search results, and Facebook and Twitter \n                    would present it where people have to scroll more before \n                    they see it. That way, fewer people would see it, but some\n                     people still would.</li>                    \n                <li><b>Inform</b> users that the item may be misleading, \n                    if it is not removed.  \n                    <br>For example, there might be a “misleading” \n                    icon next to the item that users could click on to find out\n                     more information about it.</li>                    \n            </ul>\n        '),
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='pay_attention_to_others_on_judgment',
            field=models.CharField(blank=True, choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Not sure')], default=False, max_length=5, null=True, verbose_name='In the “Judgments” section of the form, should you take into account what you think other labelers are likely to say about an item?'),
        ),
    ]
