# Generated by Django 2.2.4 on 2019-12-05 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0039_auto_20191205_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='corroboratingchoices',
            name='workflow',
            field=models.ForeignKey(blank=True, help_text='If not selected, all workflows are affected', null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='judgmentrequirementchoices',
            name='workflow',
            field=models.ForeignKey(blank=True, help_text='If not selected, all workflows are affected', null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='reducenumberofpeoplechoices',
            name='workflow',
            field=models.ForeignKey(blank=True, help_text='If not selected, all workflows are affected', null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflow.Workflow'),
        ),
    ]
