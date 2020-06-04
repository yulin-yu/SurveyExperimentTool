# Generated by Django 2.2.4 on 2019-11-07 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0023_answer_rater_answer_judgment_misleading_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_evidence',
            new_name='evidence',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_judgment',
            new_name='judgment',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_judgment_inform',
            new_name='judgment_inform',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_judgment_misleading_item',
            new_name='judgment_misleading_item',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_judgment_reduce',
            new_name='judgment_reduce',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_judgment_remove',
            new_name='judgment_remove',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_predict_a',
            new_name='predict_a',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_predict_b',
            new_name='predict_b',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='rater_answer_predict_c',
            new_name='predict_c',
        ),
        migrations.AlterField(
            model_name='workflow',
            name='type',
            field=models.CharField(choices=[('WITHOUT_EVIDENCE_URL_WORKFLOW', 'Workflow without evidence'), ('EVIDENCE_URL_INPUT_WORKFLOW', 'Evidence url based workflow'), ('EVIDENCE_URLS_JUDGMENT_WORKFLOW', 'Evidence based judgment workflow')], default='WITHOUT_EVIDENCE_URL_WORKFLOW', max_length=255),
        ),
    ]