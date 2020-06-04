# Generated by Django 2.2.4 on 2019-12-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0045_auto_20191212_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationanswer',
            name='corroborating_link',
            field=models.ManyToManyField(to='workflow.CorroboratingChoices', verbose_name='Which of the following are you supposed to enter in the field for a corroborating link?'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='judgment_requirements',
            field=models.ManyToManyField(to='workflow.JudgmentRequirementChoices', verbose_name='Which of the following are you required to do before entering your judgment? (multi-select; can select more than one)'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='labeling_hit_duration',
            field=models.CharField(choices=[('2', 'Up to 2 minutes'), ('6', 'Up to 6 minutes'), ('15', 'Up to 15 minutes')], default=False, max_length=5, verbose_name='About how long should you take, on average, to complete a labeling HIT?'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='pay_attention_to_others_on_judgment',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Not sure')], default=False, max_length=5, verbose_name='In the “Judgments” section of the form, should you take into account what you think other labelers are likely tosay about an item?'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='pay_attention_to_others_on_prediction',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Not sure')], default=False, max_length=5, verbose_name='In the “Predictions” section of the form, should you take into account what you think other labelers are likely to say about an item?'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='reduce_number_of_people',
            field=models.ManyToManyField(related_name='reduced_answers', to='workflow.ReduceNumberOfPeopleChoices', verbose_name='Which of the following are actions that would be taken if a search engine or social media platform decided to “reduce” how many people see this item? (multi-select)'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='remove_item',
            field=models.ManyToManyField(related_name='remove_answers', to='workflow.RemoveChoices', verbose_name='Which of the following are actions that would be taken if a search engine or social media platform decided to “remove” an item?'),
        ),
        migrations.AlterField(
            model_name='registrationanswer',
            name='warn_people',
            field=models.ManyToManyField(related_name='warn_answers', to='workflow.WarnPeopleChoices', verbose_name='Which of the following are actions that would be taken if a search engine or social media platform decided to “warn” people?'),
        ),
    ]
