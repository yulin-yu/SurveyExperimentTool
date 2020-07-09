import json
import logging
import random
import validators
from urllib.parse import urlparse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, HTML, Button
from django import forms
from django.forms import Form, ModelForm

from workflow.models import LabelingAnswer, QuizAnswer, DemographicsAnswer, \
    KnowledgeAnswer, ConsentAnswer, ItemURLs, TestAnswer  #add
from .fields import RangeSliderField, EvidenceUrlChoicesField

TEXT_WIDTH = 'width:300px'


class MTurkBaseForm(forms.Form):
    workerId = forms.CharField(max_length=255, widget=forms.HiddenInput,
                               required=False)
    hitId = forms.CharField(max_length=255, widget=forms.HiddenInput,
                            required=False)
    assignmentId = forms.CharField(max_length=255, widget=forms.HiddenInput,
                                   required=False)
    turkSubmitTo = forms.CharField(max_length=255, widget=forms.HiddenInput,
                                   required=False)


class BaseWorkflowForm(MTurkBaseForm, ModelForm):
    predict_inform = RangeSliderField(
        max=100, min=0, step=5,
        label='Out of 100 respondents, how many will want an action of '
              '<b>inform</b> (if the item is not removed)?',
    )
    predict_reduce = RangeSliderField(
        max=100, min=0, step=5,
        label='Out of 100 respondents, how many will want an action of '
              '<b>reduce</b> (if the item is not removed)?',
    )
    predict_remove = RangeSliderField(
        max=100, min=0, step=5,
        label='Out of 100 respondents, how many will want an action of '
              '<b>remove</b>?',
    )

    class Meta:
        model = LabelingAnswer
        widgets = {
            'evidence': forms.RadioSelect(),
            'misinformation_harm': forms.RadioSelect(),
            'take_action': forms.RadioSelect(),
            'judgment_misleading_item': forms.RadioSelect(),
            'judgment_inform': forms.RadioSelect(),
            'judgment_reduce': forms.RadioSelect(),
            'judgment_remove': forms.RadioSelect(),
        }
        exclude = ('answer_end', 'rater', 'workflow', 'evidence')

    def set_layout(self, ab_group, skip_done_button):
        self.helper = FormHelper()
        self.helper.form_tag = False  # todo: use this also for other forms
        inform_desc = '''
            <li><b>Inform users</b>.<br>
                <i>Show a "misleading" icon next to the item.</i>
            </li>
        '''
        reduce_desc = '''
            <li><b>Reduce</b> the item\u2019s audience.<br>
                <i>Show the item on the second page of Google search results,
                and lower in Facebook and Twitter feeds.</i>
            </li>
        '''
        if ab_group == 'A':
            inform_reduce_desc = f'{inform_desc}{reduce_desc}'
        else:
            inform_reduce_desc = f'{reduce_desc}{inform_desc}'
        self.layout = Layout(
            Fieldset(
                '',
                HTML('<h3>Assessment Questions</h3>'),
                'judgment_misleading_item',
                'misinformation_harm',
                css_class='hidden',
                css_id='assessment_fieldset',
            ),
            Fieldset(
                '',
                HTML(f"""
                    <h3>Action Questions</h3>
                    There are three possible actions.
                    <ul>
                        {inform_reduce_desc}
                        <li><b>Remove</b> the item.<br>
                            <i>Don\u2019t show the item at all in Google search
                            results or Facebook and Twitter feeds.</i>
                        </li>
                    </ul>
                """),
                'take_action',
                css_class='hidden',
                css_id='any_action_fieldset',
            ),
            Fieldset(
                '',
                HTML('Given that you think some action should be taken, '
                     'in your personal opinion, which of the following actions'
                     ' do you think they should take?'),
                'judgment_inform',
                'judgment_reduce',
                'judgment_remove',
                # 'judgment_additional_information',
                css_class='hidden',
                css_id='action_fieldset',
            ),
            Fieldset(
                '',
                HTML("<h3>Prediction Questions</h3>"
                     "Now we'd like you to predict what judgments other people"
                     " will make about this item. Imagine that we have "
                     "<b>100 other people from the general U.S. population</b>"
                     " doing the same task that you just did. "
                     "We will use your predictions for <b>quality control</b>,"
                     " but never your personal judgments.<br></br>"),
                HTML("<span class='invalid-feedback hidden'"
                     " id='predict_inform_error'>"
                     "This field is required:</span>"),
                'predict_inform',
                HTML("<span class='invalid-feedback hidden'"
                     " id='predict_reduce_error'>"
                     "This field is required:</span>"),
                'predict_reduce',
                HTML("<span class='invalid-feedback hidden'"
                     " id='predict_remove_error'>"
                     "This field is required:</span>"),
                'predict_remove',
                (
                    Button('done', 'Done with Predictions',
                           css_class='btn btn-primary')
                    if not skip_done_button
                    else ''
                ),
                css_class='hidden',
                css_id='prediction_fieldset',
            ),
            Fieldset(
                '',
                Field('item', type='hidden'),
                Field('answer_start', type='hidden'),
            ),
        )
        if ab_group == 'B':
            action_fields = self.layout.fields[2].fields
            action_fields[1], action_fields[2] = \
                action_fields[2], action_fields[1]
            self.fields['judgment_reduce'].label = \
                f"1{self.fields['judgment_reduce'].label[1:]}"
            self.fields['judgment_inform'].label = \
                f"2{self.fields['judgment_inform'].label[1:]}"

            prediction_fields = self.layout.fields[3].fields
            prediction_fields[1:3], prediction_fields[3:5] = \
                prediction_fields[3:5], prediction_fields[1:3]

    def __init__(self, *args, ab_group, skip_done_button=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout(ab_group, skip_done_button)
        self.helper.layout = self.layout

    def fields_required(self, fields):
        """Used for conditionally marking fields as required."""
        for field in fields:
            # print(f"checking {field}."
            #       f"\tfield = {self.cleaned_data.get(field)}")
            if self.cleaned_data.get(field) in [None, '']:
                # print(f'missing {field}')
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)

    def clear_fields(self, fields, default=None):
        """Used for conditional validation. Clear meaningless data"""
        for field in fields:
            # print(f'setting {field} to {default}')
            self.cleaned_data[field] = default

    def clean(self):
        assessment_fields = \
            ['judgment_misleading_item', 'misinformation_harm', 'take_action']
        prediction_fields = \
            ['predict_remove', 'predict_reduce', 'predict_inform']
        action_fields = \
            ['judgment_remove', 'judgment_reduce', 'judgment_inform']

        self.fields_required(assessment_fields + prediction_fields)

        take_action = self.cleaned_data.get('take_action')

        if take_action == "Yes":
            self.fields_required(action_fields)
        else:
            self.clear_fields(action_fields, False)


class WithoutEvidenceWorkflowForm(BaseWorkflowForm):  # Workflow 1
    pass


class EvidenceInputWorkflowForm(BaseWorkflowForm):  # Workflow 2
    evidence_url = forms.URLField(
        label='If Yes, please paste the link you found most relevant and '
              'convincing.',
        required=False)

    class Meta(BaseWorkflowForm.Meta):
        exclude = ('answer_end', 'rater', 'workflow',)

    def set_layout(self, ab_group, skip_done_button):
        super().set_layout(ab_group, skip_done_button)
        self.layout.fields.insert(0, Fieldset(
            '',
            HTML('<h3>Evidence</h3>'
                 "Second, take <b>up to five minutes</b> to search, "
                 "using a search engine, for"
                 " evidence that will help you judge the news item. "
                 "You should look for both <b>supporting and"
                 " challenging</b> evidence."
                 ),
            'evidence_search_terms',
            'evidence',
            'evidence_url',
            css_id='corroborating_evidence_fieldset',
        ))

    def check_search_terms(self):
        search_terms = self.cleaned_data.get('evidence_search_terms')
        if search_terms == None:
            msg = forms.ValidationError("This field is required.")
            self.add_error('evidence_search_terms', msg)

        # check for search terms minimum length
        elif search_terms and len(search_terms) < 4:
            msg = forms.ValidationError("This seems too short to be a search term. Please try again.")
            self.add_error('evidence_search_terms', msg)

    def check_url(self):
        def extract_domain_name(url_str):
            domain = urlparse(url_str).hostname
            return '.'.join(domain.split('.')[-2:])

        evidence_url = self.cleaned_data.get('evidence_url')
        item_url = self.initial.get('item').url

        # Check that it exists
        if evidence_url is None or len(evidence_url) < 3:
            msg = forms.ValidationError("This field is required.")
            self.add_error('evidence_url', msg)
        # Check that it's a well-formed URL
        elif not validators.url(evidence_url):
            msg = forms.ValidationError("This must be a valid URL (link to a web page).")
            self.add_error('evidence_url', msg)
        # Check that the domain name is not the domain name of the item
        elif extract_domain_name(evidence_url) == extract_domain_name(item_url):
            msg = forms.ValidationError("Please find an evidence link from a different source than the original news item")
            self.add_error('evidence_url', msg)
        # Check that the domain name is not a popular search engine
        elif extract_domain_name(evidence_url) in ['google.com', 'bing.com', 'duckduckgo.com']:
            msg = forms.ValidationError("Please paste a link to a specific page, not to a search engine")
            self.add_error('evidence_url', msg)

    def clean_evidence_things(self):
        self.fields_required(['evidence'])

        self.check_search_terms()

        if self.cleaned_data.get('evidence'):
            self.check_url()
        else:
            self.clear_fields(['evidence_url'])

    def clean(self):
        super().clean()
        self.clean_evidence_things()


class JudgmentForm(BaseWorkflowForm):  # Workflow 3
    evidence_url = EvidenceUrlChoicesField(
        label='Second, which of the following links provides '
              'the most convincing evidence either supporting or contradicting'
              ' claims in the original news item?')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item = self.initial.get('item')
        if item:
            choices = ItemURLs.objects.get_choices(item)
            if choices:
                # random permutation of order to avoid order effect
                random.shuffle(choices)
                none_of_above = "None of the above provides useful evidence"
                self.fields['evidence_url'].choices = \
                    [(url, f'Evidence link {i+1}')
                     for (i, url) in enumerate(choices)] + \
                    [(none_of_above, none_of_above)]
                self.fields['evidence_url'].widget.item_id = item.id
                self.fields['evidence_url'].widget.worker_id = \
                    self.initial.get('workerId')
            else:
                self.fields['evidence_url'].label = \
                    'Other raters did not find any URLs providing convincing '\
                    'evidence confirming or contradicting claims in the ' \
                    'original item. You <b>do not need to search</b> for any '\
                    'external evidence yourself. You should answer the ' \
                    'following questions based on what you saw in the item ' \
                    'itself.'
                no_links = "No links available"
                self.fields['evidence_url'].choices = [(no_links, no_links)]
                self.fields['evidence_url'].initial = no_links
                self.fields['evidence_url'].widget = \
                    forms.TextInput(attrs={'class': 'hidden'})

    def set_layout(self, ab_group, skip_done_button):
        super().set_layout(ab_group, skip_done_button)
        self.layout.fields.insert(0, Fieldset(
            '',
            HTML('<h3>Evidence</h3>'),
            'evidence_url',
            css_id='corroborating_evidence_fieldset',
        ))


class JournalistWorkflowForm(EvidenceInputWorkflowForm):  # Workflow 4
    # disabling `required` errors:
    take_action = forms.CharField(required=False, initial='')
    predict_inform = None
    predict_reduce = None
    predict_remove = None

    def set_layout(self, ab_group, skip_done_button):
        super().set_layout(ab_group, skip_done_button)
        self.layout.fields[0].fields[0] = HTML(
            '<h3>Evidence</h3>'
            "Second, search, using a search engine, for"
            " evidence that will help you judge the news item. "
            "You should look for both <b>supporting and"
            " challenging</b> evidence."
        )
        del self.layout.fields[4]
        del self.layout.fields[3]
        del self.layout.fields[2]

    def clean(self):
        assessment_fields = ['judgment_misleading_item', 'misinformation_harm']
        self.fields_required(assessment_fields)

        self.clean_evidence_things()


class FeedbackForm(MTurkBaseForm):
    pass


class QualifyForm(Form):
    pass


class QuizForm(ModelForm):
    class Meta:
        model = QuizAnswer
        widgets = {
            'judgment_requirements': forms.CheckboxSelectMultiple(),

            'pay_attention_to_others_on_judgment': forms.RadioSelect(),
            'pay_attention_to_others_on_prediction': forms.RadioSelect(),

            'corroborating_link_meaning': forms.CheckboxSelectMultiple(),

            'remove': forms.CheckboxSelectMultiple(),
            'reduce': forms.CheckboxSelectMultiple(),
            'inform': forms.CheckboxSelectMultiple(),
        }
        exclude = ('rater', 'corroborating_link_meaning')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.helper.layout = self.layout

    def set_layout(self):
        self.helper = FormHelper()
        self.layout = Layout(
            Fieldset('', 'judgment_requirements'),
            Fieldset('', 'pay_attention_to_others_on_judgment'),
            Fieldset('', 'pay_attention_to_others_on_prediction'),
            Fieldset('', 'corroborating_link_meaning'),
            Fieldset('', 'remove'),
            Fieldset('', 'reduce'),
            Fieldset('', 'inform'),
            Field('second_attempt', type='hidden'),
        )


class QuizFormWorkflow2(QuizForm):
    pass


class ConsentForm(ModelForm):
    class Meta:
        model = ConsentAnswer
        exclude = ('rater', )
        widgets = {
            'consent': forms.RadioSelect(attrs={"required": "required"}),
        }

class TestForm(ModelForm):   # new
    class Meta:
        model = TestAnswer #use
        exclude = ('rater', )
        widgets = {
            'select': forms.RadioSelect(attrs={"required": "required"}),
            'select1': forms.RadioSelect(attrs={"required": "required"}),
            'select2': forms.RadioSelect(attrs={"required": "required"}),
            'select3': forms.RadioSelect(attrs={"required": "required"}),
            'select4': forms.RadioSelect(attrs={"required": "required"}),
            'select5': forms.RadioSelect(attrs={"required": "required"}),
            'select6': forms.RadioSelect(attrs={"required": "required"}),
            'selecttime': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.helper.layout = self.layout

    def set_layout(self):
        self.helper = FormHelper()
        self.layout = Layout(
            Fieldset('''
In this training, we want you to label if the statement is civic or uncivil. we would like you to practice labeling a few comments. The point of this exercise is to help you learn a bit more about what we are looking for. After you provide your label, we’ll tell you what we said and why. Your goal is to label comments the way we would.
                <br/>
                <b>Do not look up the answers in a book or on the Internet.</b>
                <br/>
            '''),
            Fieldset(
                'question1',
                'select',
                'selecttime',
            ),
            Fieldset(
                'We label threats of violence and wishing physical or emotional harm on others as uncivil. Please label these comments as uncivil even if you are sympathetic to the writer’s position or think that the incivility is justified.',
            ),
            Fieldset(
                'question2',
                'select1',
            ),
            Fieldset(
                'You should label critiques of another person’s education, intelligence, maturity, or personal experience as uncivil when they discourage someone from contributing to the conversation, exploring an idea, or articulating a perspective. This comment is uncivil because it implies that another person doesn’t know enough to speak on the topic. The problem is not with the suggestion that relevant expertise exists, but with implying that only people with this expertise have anything worth saying. ',
            ),
            Fieldset(
                '',
                'reflect1',
            ),
            Fieldset(
                'question3',
                'select2',
            ),
            Fieldset(
                "You labeled this comment as uncivil. We agreed. We label sarcasm as uncivil when it is intended to insult an individual, an idea, or those that agree with an idea. This commenter is using sarcasm to criticize Canada’s former immigration policy and, presumably, the people who supported that policy.",
            ),

            Fieldset(
                'question4',
                'select3',
            ),
            Fieldset(
                'The comment is critical of Sanders’ supporters, implying that they don’t know how to read poll data, but it doesn’t use name calling, and it offers evidence to support the criticism. Remember, you do not have to find the evidence convincing. Be careful, though. The comment would be uncivil if it said, “I think Sanders’ supporters are ignorant”—that’s name calling—or “Not a single one of them understands how polls work”—that’s an insulting over generalization.     Also, you may have noticed that comments aren’t always easy to understand. They may include spelling mistakes or grammatical errors. Please take your time reading, and try to understand what the person who posted it meant.',
            ),
            Fieldset(
                'question5',
                'select4',
            ),
            Fieldset(
                'We label comments as uncivil if they are meant to shut down the conversation. A person might do this directly, by telling others to shut up. However, this comment works in a more subtle way. The commenter says that there’s no way that anyone could make a valid argument in favor of current immigration policies. Even if you agree, you should label this uncivil because the commenter is trying to prevent further discussion. It is not uncivil to point out logical flaws or lack of evidence for a claim. As with many of the examples above, commenters can choose civil or uncivil ways of making the same points.',
            ),
            Fieldset(
                'question6',
                'select5',
            ),
            Fieldset(
                'We do not label comments uncivil just because someone admits to hating a person, an idea, or people who agree with that idea. But please read carefully to see if they justify this disagreement in an uncivil way. Remember, it is always uncivil to use name calling or over generalization without evidence. In this case, we only know that the commenter feels strongly. Think of it this way: a civil conversation should be able to include people who despise one another. A Nazi and a Jew, or a gay person and a homophobe, should be able to speak civilly, despite their strong negative feelings for one another. This is also a good reminder that comments can be very short. If you don’t have enough context to understand what the comment means, you should label it civil.',
            ),
            Fieldset(
                'question7',
                'select6',
            ),
            Fieldset(
                'Some comments seem easy to label at first glance. In this case, it may be tempting to assume that the comment is making fun of someone, perhaps suggesting that a male candidate would give up his masculine identity in order to win votes. But you should ask yourself whether it is possible that the comment was intended civilly. Perhaps the comment was literally referring to a man undergoing a gender transition. This may be unlikely, but without more information we cannot rule it out. Think carefully about whether a comment is clearly uncivil. If you aren’t sure, label it civil. Remember, even well-intentioned comments can come across the wrong way without context. Your job is to look deeper.  ',
            ),

        )

class KnowledgeForm(ModelForm):
    class Meta:
        model = KnowledgeAnswer
        exclude = ('rater', )
        widgets = {
            'pk_1': forms.RadioSelect(),
            'pk_2': forms.RadioSelect(),
            'pk_3': forms.RadioSelect(),
            'pk_4': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.helper.layout = self.layout

    def set_layout(self):
        self.helper = FormHelper()
        self.layout = Layout(
            Fieldset('''
                In this next task, you will be asked several factual
                questions about politics and public policy.
                Many people don’t know the answers to these questions,
                but it is helpful for us if you answer,
                even if you’re not sure what the correct answer is.
                We encourage you to take a guess on every question.
                <br/>
                Please just give your best guess.
                <br/>
                <b>Do not look up the answers in a book or on the Internet.</b>
                <br/>
                You will be given 15 seconds to respond to each question
                before the survey will auto-advance.
            '''),
            Fieldset(
                'Question 1',
                'pk_1',
            ),
            Fieldset(
                'Question 2',
                'pk_2',
            ),
            Fieldset(
                'Question 3',
                'pk_3',
            ),
            Fieldset(
                'Question 4',
                'pk_4',
            ),
        )


class DemographicsForm(ModelForm):
    class Meta:
        model = DemographicsAnswer
        fields = (
            'age', 'education', 'gender', 'gender_other', 'polint',
            'polaf', 'polaf_other', 'polid', 'polid_other',
        )
        widgets = {
            'age': forms.RadioSelect(),
            'education': forms.RadioSelect(),
            'gender': forms.RadioSelect(),
            'polaf': forms.RadioSelect(),
            'polid': forms.RadioSelect(),
            'polint': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.helper.layout = self.layout

    def set_layout(self):
        self.helper = FormHelper()
        self.layout = Layout(
            Fieldset(
                '',
                'age',
                'education'
            ),
            Fieldset(
                '',
                'gender',
                'gender_other'
            ),
            Fieldset(
                '',
                'polint'
            ),
            Fieldset(
                '',
                'polaf',
                'polaf_other',
            ),
            Fieldset(
                '',
                'polid',
                'polid_other',
            ),
        )


class CongratulationsForm(MTurkBaseForm):
    pass


class ThankYouForm(MTurkBaseForm):
    pass


class MTurkAutoSendForm(MTurkBaseForm):
    pass
