import json
import logging
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Count
from django.urls import reverse

from workflow.choices import \
    JUDGMENT_MISLEADING_ITEM_CHOICES, JUDGMENT_HARM_CHOICES, \
    JUDGMENT_REMOVE_CHOICES, JUDGMENT_REDUCE_CHOICES, JUDGMENT_INFORM_CHOICES,\
    YES_NO_CHOICES, TAKE_ACTION_CHOICES, WORKFLOW_GROUPS,Test_Select
from workflow.services.mturk import mturk


class Workflow(models.Model):
    WITHOUT_EVIDENCE_URL = 1
    EVIDENCE_URL_INPUT = 2
    EVIDENCE_URLS_JUDGMENT = 3
    JOURNALIST_WORKFLOW = 4

    WORKFLOW_TYPE_CHOICES = (
        # Type 1
        ('WITHOUT_EVIDENCE_URL_WORKFLOW', 'Workflow without evidence'),
        # Type 2
        ('EVIDENCE_URL_INPUT_WORKFLOW', 'Evidence url based workflow'),
        # Type 3
        ('EVIDENCE_URLS_JUDGMENT_WORKFLOW', 'Evidence based judgment workflow'),
        # Type 4
        ('JOURNALIST_WORKFLOW', 'Journalist workflow'),
    )

    api_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    instruction = models.TextField()
    judgment_enough_information = models.TextField(null=True, blank=True)
    judgment_misleading_item = models.TextField(null=True, blank=True)
    misinformation_harm = models.TextField(null=True, blank=True)
    take_action = models.TextField(null=True, blank=True)
    judgment_remove_reduce_inform_head = models.TextField(null=True,
                                                          blank=True)
    judgment_remove = models.TextField(null=True, blank=True)
    judgment_reduce = models.TextField(null=True, blank=True)
    judgment_inform = models.TextField(null=True, blank=True)
    judgment_additional = models.TextField(null=True, blank=True)
    prediction = models.TextField()
    corroborating_question = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=WORKFLOW_TYPE_CHOICES,
                            default='WITHOUT_EVIDENCE_URL_WORKFLOW')

    @property
    def qualification(self):
        return {
            'WITHOUT_EVIDENCE_URL_WORKFLOW': 'CSMR-Labeling-1',
            'EVIDENCE_URL_INPUT_WORKFLOW': 'CSMR-Labeling-2',
            'EVIDENCE_URLS_JUDGMENT_WORKFLOW': 'CSMR-Labeling-3',
            'JOURNALIST_WORKFLOW': 'CSMR-Labeling-4',  # fixme: never used?
        }.get(self.type)

    def __str__(self):
        return f'{self.type}: {self.name}'


class RaterManager(models.Manager):
    def get_ab_group(self, workflow):
        # assign worker to group A or B round-robin style,
        # whichever has fewer people
        a_count = Rater.objects.filter(ab_group='A', workflow=workflow).count()
        b_count = Rater.objects.filter(ab_group='B', workflow=workflow).count()
        return 'B' if a_count > b_count else 'A'

    def get_defaults(self):
        # do round-robin assignment
        # based on people who passed the qualification, since we have different pass rates

        workflow = Workflow.objects.\
            exclude(pk=Workflow.JOURNALIST_WORKFLOW).\
            annotate(
                num_raters=Count('rater',
                                 filter=Q(rater__rater_group__isnull=False))
            ).\
            order_by('num_raters', 'pk').first()

        # Emergency need for more workflow2 raters...
        # workflow = Workflow.objects.get(type='EVIDENCE_URL_INPUT_WORKFLOW')

        return {
            'workflow': workflow,
            'ab_group': self.get_ab_group(workflow),
        }

    def create_default_user(self, worker_id):
        user, created = User.objects.get_or_create(username=worker_id)
        return user

    def create(self, **kwargs):
        kwargs.update(self.get_defaults())
        if not ('user' in kwargs or 'user_id' in kwargs):
            kwargs.update({
                'user': self.create_default_user(kwargs.get('worker_id'))
            })
        return super().create(**kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        defaults.update(self.get_defaults())

        self._for_write = True
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            if not ('user' in defaults or 'user_id' in defaults):
                defaults.update({
                    'user': self.create_default_user(defaults.get('worker_id'))
                })
            return super(RaterManager, self).get_or_create(defaults, **kwargs)


class Rater(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    worker_id = models.CharField(max_length=255, unique=True, blank=True,
                                 null=True)
    rejected_state = models.BooleanField(default=False)
    completed_register_state = models.BooleanField(default=False)
    completed_demographics_state = models.BooleanField(default=False)
    completed_label = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES,
                              default='f')

    location = models.CharField(max_length=255, blank=True, null=True)
    workflow = models.ForeignKey('Workflow', null=True,
                                 on_delete=models.SET_NULL)
    rater_group = models.CharField(max_length=255, blank=True, null=True)
    ab_group = models.CharField(max_length=255, blank=True, null=True)
    probation = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True, auto_now_add=True)

    objects = RaterManager()

    @property
    def rater_group_name(self):
        return f'CSMR-Labeling-{self.rater_group}'

    def rater_qualification_id(self):
        return Qualification.objects.get(name=self.rater_group_name).mturk_id

    def associate_qualification(self):
        qualification_id = self.rater_qualification_id()
        mturk.associate_qualification(self.worker_id, qualification_id,
                                      integer_value=1)

    def disassociate_qualification(self):
        try:
            qualification_id = self.rater_qualification_id()
            mturk.disassociate_qualification(self.worker_id, qualification_id)
        except Exception as e:
            logging.error(f"revoking a non-existent qualification\n {e}")

    def __str__(self):
        return f'{self.worker_id} workflow:{self.workflow}'


class ActiveItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_available(self, rater):
        return self.get_queryset().exclude(labelinganswer__rater=rater)

    def get_answered(self, rater):
        return self.get_queryset().filter(labelinganswer__rater=rater)

    def newly_ready(self):
        items = self.get_queryset().\
            exclude(itemworkflow__workflow__pk=Workflow.EVIDENCE_URLS_JUDGMENT)
        result = []
        for item in items:
            groups = ['4A', '4B', '5A', '5B', '6A', '6B']
            answers = \
                item.labelinganswer_set.filter(rater__rater_group__in=groups)
            counts = dict.fromkeys(groups, 0)
            for answer in answers:
                counts[answer.rater.rater_group] += 1
            if all([count >= 9 for key, count in counts.items()]):
                result.append(item)
        return result


class Item(models.Model):
    url = models.URLField(max_length=2000)
    category = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    active = ActiveItemManager()

    objects = models.Manager()

    def create_hits(self, workflow_id):
        from workflow.services.mturk import mturk
        workflow = Workflow.objects.get(pk=workflow_id)
        qualification_names = []
        group_numbers = WORKFLOW_GROUPS[workflow.type].values()  # ...

        for group_num in group_numbers:
            for let in ['A', 'B']:
                qualification_names.append(f'CSMR-Labeling-{group_num}{let}')

        urls = []
        for qualification_name in qualification_names:
            mturk_id = \
                Qualification.objects.get(name=qualification_name).mturk_id

            if qualification_name[-2] in ['1', '2', '3']:
                reward = "0.5"
            else:
                reward = "1.0"
            hit = mturk.register_hit(
                'labeling', self.get_absolute_url(),
                configuration_overrides={
                    "Reward": reward
                },
                extra_qualifications=[
                    {
                        "QualificationTypeId": mturk_id,
                        "Comparator": "Exists",
                        'ActionsGuarded': 'PreviewAndAccept'
                        # "RequiredToPreview": True
                    }
                ],
                title=f"{qualification_name[-2:]} Is this news item misleading?"
            )

            url = f'https://workersandbox.mturk.com' + \
                  f'/mturk/preview?groupId={hit["HITTypeId"]}'

            ItemWorkflow.objects.update_or_create(
                item=self,
                workflow=workflow,
                qualification=qualification_name,
                defaults={'hit_id': hit['HITId'], 'hit_group_url': url}
            )
            urls.append(url)
        return urls

    def set_item_urls(self):
        # select URLs to present in workflow 3 based on workflow 2 results
        """
        Examine all the corroborating URLs that were provided by raters in
        workflow 2 for this item.
            Among the liberal raters, pick the corroborating URL
                that was provided most often.
            Among the conservative raters, pick the corroborating URL
                that was provided most often.
            Among the other raters, pick the corroborating URL
                that was provided most often.
        That will determine 1-3 URLs.
        The additional URLs to reach 4 should be selected based on
            which were most popular overall (across all workflow 2 raters),
            but not yet selected.
        """
        workflow2 = \
            Workflow.objects.get(type='EVIDENCE_URL_INPUT_WORKFLOW')
        prev_answers = LabelingAnswer.objects.select_related('rater').\
            filter(Q(item=self) & Q(workflow=workflow2) & Q(evidence_url__isnull=False)).all()
        # rater groups:
        # "6A" and "6B" for conservatives; "4A" and "4B" for liberals
        liberal_answers = [
            answer
            for answer in prev_answers
            if answer.rater.rater_group and "4" in answer.rater.rater_group
        ]
        moderate_answers = [
            answer
            for answer in prev_answers
            if answer.rater.rater_group and "5" in answer.rater.rater_group
        ]
        conservative_answers = [
            answer
            for answer in prev_answers
            if answer.rater.rater_group and "6" in answer.rater.rater_group
        ]
        def get_popular_urls(answers_list):
            counts = dict()
            for ans in answers_list:
                counts[ans.evidence_url] = \
                    counts.get(ans.evidence_url, 0) + 1
            return sorted(counts, key=lambda k: counts[k], reverse=True)

        final_urls = set()
        # get single most popular from each group, including overall
        for lst in [prev_answers, liberal_answers, moderate_answers, conservative_answers]:
            most_popular_urls = get_popular_urls(lst)
            if len(most_popular_urls) > 0:
                final_urls.add(most_popular_urls[0])

        # # now fill in with overall most popular, up to 3 total
        # for pop_url in get_popular_urls(prev_answers):
        #     if len(final_urls) >= 3:
        #         break
        #     else:
        #         final_urls.add(pop_url)

        ItemURLs(
            item=self,
            prev_urls=json.dumps(list(final_urls))
        ).save()

    def set_item_counts(self):
        item = self
        for workflow in Workflow.objects.all():
            ItemAnswers.objects.create_counts(item, workflow).save()

    def url_quoted(self):  # for redirect URL
        return quote(self.url)

    def get_absolute_url(self):
        return reverse('workflow:item', kwargs={'pk': self.pk})

    def __str__(self):
        return f'URL: {self.url} (ID: {self.pk})'


class ItemWorkflow(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE)
    hit_group_url = models.CharField(max_length=255, null=True, blank=True)
    hit_id = models.CharField(max_length=255, null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f'{self.workflow.qualification}: {self.qualification}: ' \
               f'{self.hit_id}'


class ItemURLsManager(models.Manager):
    def get_choices(self, item):
        obj = ItemURLs.objects.filter(item=item).order_by('pk').last()
        if obj:
            return json.loads(obj.prev_urls)
        else:
            logging.error(f'Trying to show URL choices for an Item even '
                          f'though not yet set. Should be set when the HIT'
                          f' for workflow 3 is created.')
            return []


class ItemURLs(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    prev_urls = models.CharField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    objects = ItemURLsManager()

    def __str__(self):
        return f'{self.item.url}: {self.prev_urls}'


class ItemAnswersManager(models.Manager):
    def get_counts(self, item, workflow, rater):
        data = self.filter(item=item, workflow=workflow).order_by('pk').last()
        if data:
            return data
        return self.create_counts(item, workflow, rater)

    def create_counts(self, item, workflow, rater=None):
        answers = LabelingAnswer.objects.filter(item=item, workflow=workflow).\
            exclude(take_action='Not enough info')
        if rater:
            answers = answers.exclude(rater=rater)
        return ItemAnswers(
            item=item,
            workflow=workflow,
            total_simulated_answers=len(answers),
            inform_count=len([a for a in answers if a.judgment_inform]),
            reduce_count=len([a for a in answers if a.judgment_reduce]),
            remove_count=len([a for a in answers if a.judgment_remove]),
        )


class ItemAnswers(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE)
    inform_count = models.IntegerField(null=True, blank=True)
    reduce_count = models.IntegerField(null=True, blank=True)
    remove_count = models.IntegerField(null=True, blank=True)
    total_simulated_answers = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    objects = ItemAnswersManager()

    class Meta:
        verbose_name_plural = 'Item answers'  # for admin panel


class RedirectLinkClickedManager(models.Manager):
    def get_status(self, rater, item):
        entries = self.filter(rater=rater, item=item)
        item_link_clicked = \
            entries.filter(item_link_clicked=True).last() is not None
        corroborating_link_clicked = \
            entries.filter(corroborating_link_clicked=True).last() is not None
        return item_link_clicked, corroborating_link_clicked


class RedirectLinkClicked(models.Model):
    rater = models.ForeignKey('Rater', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    item_link_clicked = models.BooleanField(default=False, null=True,
                                            blank=True)
    corroborating_link_clicked = models.BooleanField(default=False, blank=True,
                                                     null=True)
    clicked_at = models.DateTimeField(null=True, auto_now_add=True)

    objects = RedirectLinkClickedManager()


class LabelingAnswer(models.Model):
    rater = models.ForeignKey('Rater', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE)
    answer_start = models.DateTimeField()
    answer_end = models.DateTimeField()
    evidence = models.BooleanField(
        default=None,
        choices=YES_NO_CHOICES, null=True, blank=True,
        verbose_name="<br>Did you find any page with evidence you found"
                     " convincing, one way or the other?</br>")
    evidence_url = models.CharField(max_length=512, null=True, blank=True)
    evidence_search_terms = models.CharField(max_length=512, null=True, blank=True,
                                             verbose_name = "What search terms did you use?")

    judgment_misleading_item = models.PositiveIntegerField(
        default=None,
        choices=JUDGMENT_MISLEADING_ITEM_CHOICES,
        blank=True,
        null=True,
        verbose_name="How misleading is this news item?"
    )
    misinformation_harm = models.PositiveIntegerField(
        default=None,
        choices= JUDGMENT_HARM_CHOICES,
        blank=True,
        null=True,
        verbose_name='How much harm would there be if people were misinformed '
                     'about the topic of this news item?'
    )

    take_action = models.CharField(
        max_length = 32,
        default=None,
        choices=TAKE_ACTION_CHOICES,
        null=True,
        verbose_name= """
            Based on your answers to the last two questions
            (misinformation and harm), in your personal opinion do you think
            that social media platforms and search engines should take
            <b>at least one of these actions</b> on this item?
        """
    )

    judgment_inform = models.BooleanField(
        default=None,
        choices=JUDGMENT_INFORM_CHOICES,
        null=True,
        blank=True,
        verbose_name="1. <b>Inform</b> users that the item may be misleading. "
                     "(Assuming it is not removed.)")
    judgment_reduce = models.BooleanField(
        default=None,
        choices=JUDGMENT_REDUCE_CHOICES,
        null=True,
        blank=True,
        verbose_name="2. <b>Reduce</b> the item\u2019s audience. "
                     "(Assuming it is not removed.)")
    judgment_remove = models.BooleanField(
        default=None,
        choices=JUDGMENT_REMOVE_CHOICES,
        null=True,
        blank=True,
        verbose_name="3. <b>Remove</b> the item."
        )



    judgment_additional_information = models.TextField(blank=True, null=True)

    predict_remove = models.IntegerField(default=None, blank=True, null=True)
    predict_reduce = models.IntegerField(default=None, blank=True, null=True)
    predict_inform = models.IntegerField(default=None, blank=True, null=True)

    item_link_clicked = models.BooleanField(default=False, null=True,
                                            blank=True)  # todo: remove later
    corroborating_link_clicked = models.BooleanField(default=False, blank=True,
                                                     null=True)  # todo: remove

    def __str__(self):
        return f'rater:{self.rater} item:{self.item} workflow:{self.workflow}'


class ChoiceModelAbstract(models.Model):
    title = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        # if settings.DEBUG:
        #     is_correct = self.is_correct and 'correct' or 'incorrect'
        #     return f'{self.title} ({is_correct})'
        return self.title

    class Meta:
        abstract = True


class ReduceChoices(ChoiceModelAbstract):
    pass


class InformChoices(ChoiceModelAbstract):
    pass


class RemoveChoices(ChoiceModelAbstract):
    pass


class JudgmentRequirementChoices(ChoiceModelAbstract):
    correct_for_workflows = models.ManyToManyField(Workflow)


class CorroboratingChoices(ChoiceModelAbstract):
    correct_for_workflows = models.ManyToManyField(Workflow)
    pass


class QuizAnswer(models.Model):
    YES_NO_NOT_SURE_CHOICES = (
        ('self', 'My personal opinion about what search engines and '
                 'social media platforms should do'),
        ('others', 'What I think others will say the search engines and '
                   'social media platforms should do'),
        ('NoTB', 'Neither of these')
    )

    rater = models.ForeignKey('Rater', on_delete=models.CASCADE)

    remove = models.ManyToManyField(
        RemoveChoices,
        verbose_name='As we described it, what does <b>remove</b> mean?'
                     '<br><b>(Check all that apply)</b></br>',
        related_name='remove_answers',
        blank=True,
    )
    reduce = models.ManyToManyField(
        ReduceChoices,
        verbose_name='As we described it, what does <b>reduce</b> mean?'
                     '<br><b>(Check all that apply)</b></br>',
        related_name='reduce_answers',
        blank=True,
    )

    inform = models.ManyToManyField(
        InformChoices,
        verbose_name='As we described it, what does <b>inform</b> mean?'
                     '<br><b>(Check all that apply)</b></br>',
        related_name='inform_answers',
        blank=True,
    )

    pay_attention_to_others_on_judgment = models.CharField(
        default=False,
        max_length=255,
        choices=YES_NO_NOT_SURE_CHOICES,
        verbose_name='In the "Action Questions" section '
                     'of the form, which should you report?',
        null=True, blank=True,
    )

    pay_attention_to_others_on_prediction = models.CharField(
        max_length=255,
        default=False,
        choices=YES_NO_NOT_SURE_CHOICES,
        verbose_name='In the "Prediction Questions" section of the form, '
                     'which should you report?',
        null=True, blank=True,
    )

    judgment_requirements = models.ManyToManyField(
        JudgmentRequirementChoices,
        verbose_name='What do we expect you to do before answering '
                     'the assessment questions?'
                     '<br><b>(Check all that apply)</b></br>',
        blank=True,
    )

    corroborating_link_meaning = models.ManyToManyField(
        CorroboratingChoices,
        verbose_name='Suppose that '
                     'you <b>searched on Google</b> for "Cupping treatment cancer", '
                     'and that you found convincing evidence at '
                     'https://www.cancer.gov/about-cancer/. '
                     '<b>What should you have pasted as an evidence link</b> in the form above?'
                     '<br><b>(Check all that apply)</b></br>',


        blank=True,
    )

    second_attempt = models.BooleanField(default=False, null=True, blank=True)
    closed = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def check_multi_choices(self, query_1, query_2, workflow_specific=False):
        answered = set(query_1.values_list('pk', flat=True))
        if workflow_specific:
            correct = query_2.filter(correct_for_workflows=self.rater.workflow)
        else:
            correct = query_2.filter(is_correct=True)
        correct = set(correct.values_list('pk', flat=True))
        return answered == correct

    @property
    def passes_judgment_requirements(self):
        return self.check_multi_choices(self.judgment_requirements,
                                        JudgmentRequirementChoices.objects,
                                        workflow_specific=True)

    @property
    def passes_judgement(self):
        return self.pay_attention_to_others_on_judgment == 'self'

    @property
    def passes_prediction(self):
        return self.pay_attention_to_others_on_prediction == 'others'

    @property
    def passes_remove(self):
        return self.check_multi_choices(self.remove, RemoveChoices.objects)

    @property
    def passes_reduce(self):
        return self.check_multi_choices(self.reduce, ReduceChoices.objects)

    @property
    def passes_inform(self):
        return self.check_multi_choices(self.inform, InformChoices.objects)

    @property
    def is_test_passed(self):
        return self.passes_judgment_requirements and \
               self.passes_judgement and \
               self.passes_prediction and \
               self.passes_remove and \
               self.passes_reduce and \
               self.passes_inform


class TestAnswer(models.Model):
    rater = models.ForeignKey('Rater', on_delete=models.CASCADE) # which user answer which question

    select = models.CharField(
        max_length=10,
        verbose_name="Of course I hope he suffers. He not only hates gay men, but he targets LGBT children, who already have a high rate of homelessness and mental health issues caused by stress. He supports “conversion therapy,” a form of torture. He would allow local grocery stores and restaurants to refuse to serve an LGBT person, which would disproportionately impact rural LGBT youth. If there were a way to knock some empathy into him, I wish someone would do it. Why am I supposed to want to protect someone who seeks to hurt us?" ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )

    #select = models.CharField(
    #    max_length =10,
    #    default=None,
    #    choices=Test_Select,  # where are these come from
    #    null=True,
    #    blank=True,
    #    verbose_name="Of course I hope he suffers. He not only hates gay men, but he targets LGBT children, who already have a high rate of homelessness and mental health issues caused by stress. He supports “conversion therapy,” a form of torture. He would allow local grocery stores and restaurants to refuse to serve an LGBT person, which would disproportionately impact rural LGBT youth. If there were a way to knock some empathy into him, I wish someone would do it. Why am I supposed to want to protect someone who seeks to hurt us?"   # need to change this?
    #    )
    select1 = models.CharField(
        max_length=10,
        verbose_name="You give me all these moral arguments about social welfare and the economy. However, all of the actual economists I know (including ones from Oxford University) are libertarians. Perhaps you just aren’t educated enough to talk about this issue?" ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )

    select2 = models.CharField(
        max_length=10,
        verbose_name="[Canada to lift visa requirements for Mexico](http://www.pm.gc.ca/eng/news/2016/06/28/canada-lift-visa-requirements-mexico) Holy crap, immigration policy can *evolve*? What a wild concept." ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )

    select3 = models.CharField(
        max_length=10,
        verbose_name="The funny thing about Michigan is that it had a 99% certainty, which would mean you would expect it to get called wrong roughly once every 100 times. Well as it happens, that's almost exactly the record that places like fivethirtyeight have had: giving one incorrect result out of the few hundred they've made predictions on. So at no point should anybody suspect that the polling is systematically failing. And yet so so so many Bernie supporters pull out poll data on Bernie's side like it was some kind of Trump card. I read an editorial making the same flawed point yesterday and I just read three people making that flawed argument, today!" ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )

    select4 = models.CharField(
        max_length=10,
        verbose_name="I don’t get how any sane person could argue that immigration isn’t a problem. Over half a million competent well paid technical people were displaced by H1B visa workers in the last few years. Those displaced workers either are still unemployed, or underemployed, and thanks to losing their jobs, collected unemployment benefits. There’s no way that pro-immigration people can argue that American citizens should continue to support these lax immigration policies. " ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )

    select5 = models.CharField(
        max_length=10,
        verbose_name=" I detest Hillary Clinton and the people who voted for her.  " ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )

    select6 = models.CharField(
        max_length=10,
        verbose_name="By the time he made it to the top, his gender transition would be complete." ,
        choices=(
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),

        ),
        null=True, blank=True,
    )
    reflect1 = models.CharField(
        max_length=500,
        verbose_name="input sth" ,
        null=True, blank=True,
    )

    created_at = models.DateTimeField(null=True, auto_now_add=True)

    selecttime = models.CharField(
        max_length=500,
        verbose_name="input sth" ,
        null=True, blank=True,
    )



class ConsentAnswer(models.Model):
    rater = models.ForeignKey('Rater', on_delete=models.CASCADE)

    consent = models.CharField(
        default=False,
        max_length=5,
        verbose_name='This is a research study at the University of Michigan. '
                     'Please view the '
                     '<a href="https://drive.google.com/file/d/'
                     '14S-hc5mcXP0BfGDymJcGAmCW1nG6quUW/view?usp=sharing" '
                     'target="_blank">consent form</a>, read it, '
                     'and then indicate whether you consent to participate '
                     'in the study, by clicking below.',
        choices=(
            ('y', 'Yes, I consent to participate in this study'),
            ('n', 'No, I do not consent to participate in this study'),
        ),
    )

    created_at = models.DateTimeField(null=True, auto_now_add=True)

    @property
    def is_test_passed(self):
        return self.consent == 'y'


class KnowledgeAnswer(models.Model):
    rater = models.ForeignKey('Rater', on_delete=models.CASCADE)

    pk_1 = models.CharField(
        max_length=5,
        verbose_name='Whose responsibility is it to decide if a law '
                     'is constitutional or not?',
        choices=(
            ('1', 'The President'),
            ('2', 'Congress'),
            ('3', 'The Supreme Court'),
        ),
        null=True, blank=True,
    )

    pk_2 = models.CharField(
        max_length=5,
        verbose_name='Whose responsibility is it to nominate judges to '
                     'Federal Courts?',
        choices=(
            ('1', 'The President'),
            ('2', 'Congress'),
            ('3', 'The Supreme Court'),
        ),
        null=True, blank=True,
    )

    pk_3 = models.CharField(
        max_length=5,
        verbose_name='Who is the leader of the Labour Party of Great Britain? '
                     'Is it:',
        choices=(
            ('1', 'Theresa May'),
            ('2', 'Jeremy Corbyn'),
            ('3', 'Tony Hayward'),
            ('4', 'Boris Johnson'),
        ),
        null=True, blank=True,
    )

    pk_4 = models.CharField(
        max_length=5,
        verbose_name='What job or political office is currently '
                     'held by Nancy Pelosi? Is it:',
        choices=(
            ('1', 'Speaker of the House'),
            ('2', 'Treasury Secretary'),
            ('3', 'Senate Majority Leader'),
            ('4', 'Justice of the Supreme Court'),
            ('5', 'Governor of New Mexico'),
        ),
        null=True, blank=True,
    )

    created_at = models.DateTimeField(null=True, auto_now_add=True)

    @property
    def is_test_passed(self):
        correct_answers = sum([
            self.pk_1 == '3',
            self.pk_2 == '1',
            self.pk_3 == '2',
            self.pk_4 == '1',
        ])
        return correct_answers >= 2


class DemographicsAnswer(models.Model):
    rater = models.ForeignKey('Rater', on_delete=models.CASCADE)

    crt1_1 = models.CharField(
        max_length=255,
        verbose_name='The ages of Mark and Adam add up to 28 years total. '
                     'Mark is 20 years older than Adam. '
                     'How many years old is Adam?',
        null=True, blank=True,
    )

    crt1_2 = models.CharField(
        max_length=255,
        verbose_name='If it takes 10 seconds for 10 printers to print out '
                     '10 pages of paper, how many seconds will it take '
                     '50 printers to print out 50 pages of paper?',
        null=True, blank=True,
    )

    crt1_3 = models.CharField(
        max_length=255,
        verbose_name='On a loaf of bread, there is a patch of mold. '
                     'Every day, the patch doubles in size. '
                     'If it takes 40 days for the patch to cover the entire '
                     'loaf of bread, how many days would it take for the patch'
                     ' to cover half of the loaf of bread?',
        null=True, blank=True,
    )

    crt3_1 = models.CharField(
        max_length=255,
        verbose_name='If you’re running a race and you pass the person '
                     'in second place, what place are you in?',
        null=True, blank=True,
    )

    crt3_2 = models.CharField(
        max_length=255,
        verbose_name='A farmer had 15 sheep and all but 8 died. '
                     'How many are left?',
        null=True, blank=True,
    )

    crt3_3 = models.CharField(
        max_length=255,
        verbose_name='Emily’s father has three daughters. '
                     'The first two are named April and May. '
                     'What is the third daughter’s name?',
        null=True, blank=True,
    )

    crt3_4 = models.CharField(
        max_length=255,
        verbose_name='How many cubic feet of dirt are there in a hole '
                     'that is 3’ deep x 3’ wide x 3’ long?',
        null=True, blank=True,
    )

    polint = models.CharField(
        max_length=5,
        verbose_name='Would you say you follow what’s going on in government '
                     'and public affairs:',
        choices=(
            (None, ''),
            ('1', 'most of the time'),
            ('2', 'some of the time'),
            ('3', 'only now and then'),
            ('4', 'hardly at all'),
        ),
        default=False
    )

    polaf = models.CharField(
        max_length=5,
        verbose_name='Generally speaking, when it comes to political parties '
                     'in the United States, how would you best describe '
                     'yourself?',
        choices=(
            (None, ''),
            ('1', 'A Strong Democrat'),
            ('2', 'A Not Very Strong Democrat'),
            ('3', 'Independent, lean toward Democrat'),
            ('4', 'Independent (close to neither party)'),
            ('5', 'Independent, lean toward Republican'),
            ('6', 'A Not Very Strong Republican'),
            ('7', 'Strong Republican'),
            ('_', 'Something else, please specify'),
        ),
        null=True, default=False
    )

    polaf_other = models.CharField(
        max_length=255,
        verbose_name='Specify something else',
        null=True, blank=True,
    )

    polid = models.CharField(
        max_length=5,
        verbose_name='Now when thinking about politics, how would you describe'
                     ' your political views?',
        choices=(
            (None, ''),
            ('1', 'Very Liberal'),
            ('2', 'Liberal'),
            ('3', 'Somewhat Liberal'),
            ('4', 'Moderate or Middle of the Road'),
            ('5', 'Somewhat Conservative'),
            ('6', 'Conservative'),
            ('7', 'Very Conservative'),
            ('_', 'Something else, please specify'),
        ),
        null=True,
    )

    polid_other = models.CharField(
        max_length=255,
        verbose_name='Specify something else',
        null=True, blank=True,
    )

    ecoid = models.CharField(
        max_length=5,
        verbose_name='Now when thinking about economic issues, how would you '
                     'describe your political views?',
        choices=(
            ('1', 'Very Liberal'),
            ('2', 'Liberal'),
            ('3', 'Somewhat Liberal'),
            ('4', 'Moderate or Middle of the Road'),
            ('5', 'Somewhat Conservative'),
            ('6', 'Conservative'),
            ('7', 'Very Conservative'),
            # ('_', 'Something else, please specify'),  # todo
        ),
        null=True, blank=True,
    )

    socid = models.CharField(
        max_length=5,
        verbose_name='Now when thinking about social issues, how would you '
                     'describe your political views?',
        choices=(
            ('1', 'Very Liberal'),
            ('2', 'Liberal'),
            ('3', 'Somewhat Liberal'),
            ('4', 'Moderate or Middle of the Road'),
            ('5', 'Somewhat Conservative'),
            ('6', 'Conservative'),
            ('7', 'Very Conservative'),
            # ('_', 'Something else, please specify'),  # todo
        ),
        null=True, blank=True,
    )

    age = models.CharField(
        max_length=5,
        verbose_name='What is your age?',
        choices=(
            (None, ''),
            ('< 18', 'Under 18 years old'),
            ('18-29', '18-29 years old'),
            ('30-39', '30-39 years old'),
            ('40-49', '40-49 years old'),
            ('50-59', '50-59 years old'),
            ('> 60', '60 years or older'),
        ),
        null=True, default=False
    )

    gender = models.CharField(
        max_length=5,
        verbose_name='What is your gender?',
        choices=(
            (None, ''),
            ('f', 'Female'),
            ('m', 'Male'),
            ('3', 'Non-binary / third gender'),
            ('_', 'Prefer to self-describe'),
            ('x', 'Prefer not to say'),
        ),
        null=True, default=False
    )

    gender_other = models.CharField(
        max_length=255,
        verbose_name='Self-described gender',
        null=True, blank=True,
    )

    education = models.CharField(
        max_length=5,
        verbose_name='What is the highest level of school you have completed '
                     'or the highest degree you have received?',
        choices=(
            (None, ''),
            ('1', 'Less than high school degree'),
            ('2', 'High school degree or equivalent (e.g., GED)'),
            ('3', 'Some college but no degree'),
            ('4', 'Associate degree'),
            ('5', 'Bachelor degree'),
            ('6', 'Graduate degree'),
        ),
        null=True, default=False
    )

    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def get_political_lean(self):
        if self.polaf in ['1', '2', '3'] and self.polid in ['1', '2', '3']:
            return "Liberal"
        elif self.polaf in ['5', '6', '7'] and self.polid in ['5', '6', '7']:
            return "Conservative"
        else:
            return "Moderate"

    @property
    def is_test_passed(self):
        return True  # always pass


class Assignment(models.Model):  # todo: remove, never used
    assignment_id = models.CharField(max_length=255, unique=True)
    hit_id = models.CharField(max_length=255)
    rater = models.ForeignKey(Rater, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'assignment:{self.assignment_id} hit:{self.hit_id} ' \
               f'rater:{self.rater}'


class Qualification(models.Model):
    name = models.CharField(max_length=255)
    mturk_id = models.CharField(max_length=255)
