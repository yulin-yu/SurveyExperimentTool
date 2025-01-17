# Generated by Django 2.2.4 on 2020-01-23 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0052_merge_20200120_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationanswer',
            name='consent',
            field=models.CharField(choices=[('y', 'Yes, I consent to participate in this study'), ('n', 'No, I do not consent to participate in this study')], default=False, max_length=5, verbose_name='This is a research study at the University of Michigan. Please view the <a href="https://drive.google.com/file/d/14S-hc5mcXP0BfGDymJcGAmCW1nG6quUW/view?usp=sharing" target="_blank">contest form</a>, read it, and then indicate whether you consent to participate in the study, by clicking below.'),
        ),
    ]
