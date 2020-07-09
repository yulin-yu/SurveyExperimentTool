# Generated by Django 2.2.10 on 2020-07-08 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0099_auto_20200603_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='testanswer',
            name='reflect1',
            field=models.CharField(blank=True, max_length=5000000, null=True, verbose_name='input sth'),
        ),
        migrations.AddField(
            model_name='testanswer',
            name='select3',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name="The funny thing about Michigan is that it had a 99% certainty, which would mean you would expect it to get called wrong roughly once every 100 times. Well as it happens, that's almost exactly the record that places like fivethirtyeight have had: giving one incorrect result out of the few hundred they've made predictions on. So at no point should anybody suspect that the polling is systematically failing. And yet so so so many Bernie supporters pull out poll data on Bernie's side like it was some kind of Trump card. I read an editorial making the same flawed point yesterday and I just read three people making that flawed argument, today!"),
        ),
        migrations.AddField(
            model_name='testanswer',
            name='select4',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name='I don’t get how any sane person could argue that immigration isn’t a problem. Over half a million competent well paid technical people were displaced by H1B visa workers in the last few years. Those displaced workers either are still unemployed, or underemployed, and thanks to losing their jobs, collected unemployment benefits. There’s no way that pro-immigration people can argue that American citizens should continue to support these lax immigration policies. '),
        ),
        migrations.AddField(
            model_name='testanswer',
            name='select5',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name=' I detest Hillary Clinton and the people who voted for her.  '),
        ),
        migrations.AddField(
            model_name='testanswer',
            name='select6',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name='By the time he made it to the top, his gender transition would be complete.'),
        ),
        migrations.AlterField(
            model_name='testanswer',
            name='select',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name='Of course I hope he suffers. He not only hates gay men, but he targets LGBT children, who already have a high rate of homelessness and mental health issues caused by stress. He supports “conversion therapy,” a form of torture. He would allow local grocery stores and restaurants to refuse to serve an LGBT person, which would disproportionately impact rural LGBT youth. If there were a way to knock some empathy into him, I wish someone would do it. Why am I supposed to want to protect someone who seeks to hurt us?'),
        ),
        migrations.AlterField(
            model_name='testanswer',
            name='select1',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name='You give me all these moral arguments about social welfare and the economy. However, all of the actual economists I know (including ones from Oxford University) are libertarians. Perhaps you just aren’t educated enough to talk about this issue?'),
        ),
        migrations.AlterField(
            model_name='testanswer',
            name='select2',
            field=models.CharField(blank=True, choices=[(None, ''), ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'), ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.')], max_length=5, null=True, verbose_name='[Canada to lift visa requirements for Mexico](http://www.pm.gc.ca/eng/news/2016/06/28/canada-lift-visa-requirements-mexico) Holy crap, immigration policy can *evolve*? What a wild concept.'),
        ),
    ]
