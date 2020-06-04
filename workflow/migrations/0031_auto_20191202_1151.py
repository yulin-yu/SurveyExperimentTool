# Generated by Django 2.2.4 on 2019-12-02 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0030_rater_qualification'),
    ]

    operations = [
        migrations.CreateModel(
            name='JudgmentRequirementChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ReduceNumberOfPeopleChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='answer',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workflow.Item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='rater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Rater'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Workflow'),
        ),
        migrations.CreateModel(
            name='RegistrationAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_attention_to_others_on_judgment', models.NullBooleanField(verbose_name='In the “Judgments” section of the form, should you take into account what you think other labelers are likely tosay about an item?')),
                ('pay_attention_to_others_on_prediction', models.NullBooleanField(verbose_name='In the “Predictions” section of the form, should you take into account what you think other labelers are likely to say about an item?')),
                ('labeling_hit_duration', models.CharField(choices=[('2', 'Up to 2 minutes'), ('6', 'Up to 6 minutes'), ('15', 'Up to 15 minutes')], max_length=5, verbose_name='About how long should you take, on average, to complete a labeling HIT?')),
                ('corroborating_link', models.CharField(choices=[('news_url', 'The URL for the news item you are making a judgment about'), ('search_query', 'The URL for the search query you ran'), ('domain_name', 'The domain name of the news items (e.g., foxnews.com)'), ('search_engine', 'The name of the search engine you used'), ('same_topic_url', 'The URL for a different page that also has information about the same topic as the news item'), ('fact_checking_service', 'The domain name of a fact-checking service that you think should investigate this item.')], max_length=25, verbose_name='Which of the following are you supposed to enter in the field for a corroborating link?')),
                ('judgment_requirements', models.ManyToManyField(to='workflow.JudgmentRequirementChoices', verbose_name='Which of the following are you required to do before entering your judgment? (multi-select; can select more than one)')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Rater')),
                ('reduce_number_of_people', models.ManyToManyField(related_name='reduced_answers', to='workflow.ReduceNumberOfPeopleChoices', verbose_name='Which of the following are actions that would be taken if a search engine or social media platform decided to “reduce” how many people see this item? (multi-select)')),
                ('remove_item', models.ManyToManyField(related_name='remove_answers', to='workflow.ReduceNumberOfPeopleChoices', verbose_name='Which of the following are actions that would be taken if a search engine or social media platform decided to “remove” an item?')),
                ('warn_people', models.ManyToManyField(related_name='warn_answers', to='workflow.ReduceNumberOfPeopleChoices', verbose_name='Which of the following are actions that would be taken if a search engine or social media platform decided to “warn” people?')),
            ],
        ),
    ]
