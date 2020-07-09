from functools import wraps
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, FormView, \
    RedirectView

from . import alerts
from .choices import WORKFLOW_GROUPS
from .form import QuizForm, DemographicsForm, QuizFormWorkflow2, \
    EvidenceInputWorkflowForm, JudgmentForm, WithoutEvidenceWorkflowForm, \
    CongratulationsForm, QualifyForm, KnowledgeForm, ConsentForm, \
    ThankYouForm, FeedbackForm, JournalistWorkflowForm, MTurkAutoSendForm,TestForm
from .models import Rater, Workflow, LabelingAnswer, Item, \
    QuizAnswer, ItemAnswers, RedirectLinkClicked, ItemURLs
from .utils import dump_configurations

NONE_OF_THE_ABOVE_TUPLE = (None, 'None of the above provides useful evidence')
VERSION = settings.VERSION  # fixme: variable never used, let's use it?


def rater_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.user.rater
        except Rater.DoesNotExist:
            path = request.build_absolute_uri()
            messages.warning(request,
                             alerts.NOT_SIGNED_IN_USER_WORKFLOW_ALERTS)
            return redirect_to_login(path)
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view


class RaterWorkflowMixin:
    @cached_property
    def rater(self):
        return self.request.user.rater

    @cached_property
    def workflow(self):
        return self.rater.workflow

    @cached_property
    def ab_group(self):
        if self.rater and self.rater.ab_group in ['A', 'B']:
            return self.rater.ab_group
        else:
            # default; shouldn't happen
            message = \
                f"self.rater should be set and should be either 'A' or 'B'. " \
                f"Current it is {self.rater.ab_group}"
            logging.error(message)
            return "A"


class ForwardRedirectArguments:
    def get_url_with_params(self, url):
        assignmentId = self.request.GET.get('assignmentId')
        hitId = self.request.GET.get('hitId')
        workerId = self.request.GET.get('workerId')
        turkSubmitTo = self.request.GET.get('turkSubmitTo')
        return f'{url}?assignmentId={assignmentId}&hitId={hitId}&' \
               f'workerId={workerId}&turkSubmitTo={turkSubmitTo}'

    def get_success_url(self):
        success_url = super().get_success_url()
        return self.get_url_with_params(success_url)

    def get_fail_url(self):
        return self.get_url_with_params(reverse('workflow:thankyou'))


class WorkflowMixin(RaterWorkflowMixin):
    form_classes = {
        'WITHOUT_EVIDENCE_URL_WORKFLOW': WithoutEvidenceWorkflowForm,
        'EVIDENCE_URL_INPUT_WORKFLOW': EvidenceInputWorkflowForm,
        'EVIDENCE_URLS_JUDGMENT_WORKFLOW': JudgmentForm,
        'JOURNALIST_WORKFLOW': JournalistWorkflowForm,
    }

    def get_item(self, item_id=None):
        try:
            return Item.active.get_available(self.rater).\
                get(pk=item_id or self.kwargs.get('pk'))
        except Item.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'workflow': self.workflow,
            'rater': self.rater,
            'item': self.get_item(),
            'worker_id': self.request.GET.get('workerId'),
        })
        return context

    def get(self, request, *args, **kwargs):
        if self.workflow.type not in self.form_classes:
            messages.error(request, alerts.INVALID_WORKFLOW_ALERTS)
        return super().get(request, *args, **kwargs)


class RedirectToNextMixin:
    def get_answered_item(self):
        form_class = self.get_form_class()
        return form_class._meta.model.objects.get(rater=self.rater)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.get_answered_item()
        except ObjectDoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        if not self.object.is_test_passed:
            return HttpResponseRedirect(self.get_fail_url())
        return HttpResponseRedirect(self.get_success_url())


class SaveAnswerMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.rater = self.rater
        self.object.save()


class FeedbackMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item_id = self.request.GET.get('item') or self.request.POST.get('item')
        item = Item.objects.get(pk=item_id) if item_id else self.get_item()

        data = ItemAnswers.objects.get_counts(item, self.workflow, self.rater)
        labelers_count = data.total_simulated_answers

        if labelers_count:
            remove_percent = round(data.remove_count * 100 / labelers_count)
            reduce_percent = round(data.reduce_count * 100 / labelers_count)
            inform_percent = round(data.inform_count * 100 / labelers_count)
        else:
            remove_percent = reduce_percent = inform_percent = 0

        context.update({
            'labelers_count': labelers_count,
            'remove': {
                'your': self.request.POST.get('predict_remove', None),
                'count': data.remove_count,
                'percent': remove_percent,
            },
            'reduce': {
                'your': self.request.POST.get('predict_reduce', None),
                'count': data.reduce_count,
                'percent': reduce_percent,
            },
            'inform': {
                'your': self.request.POST.get('predict_inform', None),
                'count': data.inform_count,
                'percent': inform_percent,
            },
            'ab_group': self.ab_group,
        })
        return context


decorators = [login_required, rater_required, #xframe_options_exempt,
              csrf_exempt]


class HomeView(TemplateView):
    template_name = 'workflow/home.html'


@method_decorator(decorators, name='dispatch')
class DumpConfView(View):
    def get(self, request, *args, **kwargs):
        dump_configurations()
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; ' \
                                          'filename=configurations.json'
        with open('fixtures/configurations.json') as f:
            response.write(f.read())
        return response


@method_decorator(decorators, name='dispatch')
class ErrorView(TemplateView):
    template_name = 'workflow/error.html'


class BaseLastStepView(FormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'MTURK_WORKER_ENDPOINT': settings.MTURK_WORKER_ENDPOINT,
        })
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'workerId': self.request.GET.get('workerId'),
            'hitId': self.request.GET.get('hitId'),
            'assignmentId': self.request.GET.get('assignmentId'),
            'turkSubmitTo': self.request.GET.get('turkSubmitTo'),
        })
        return initial


@method_decorator(decorators, name='dispatch')
class RedirectLinkView(RaterWorkflowMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        click_type = self.request.GET.get('click_type')
        RedirectLinkClicked.objects.create(
            rater=self.rater,
            item_id=self.request.GET.get('item_id'),
            item_link_clicked=(click_type == 'item_link'),
            corroborating_link_clicked=(click_type == 'corroborating_link'),
        )
        return self.request.GET.get('to')


@method_decorator(decorators, name='dispatch')
class WorkflowFormView(FeedbackMixin, ForwardRedirectArguments, WorkflowMixin,
                       CreateView):
    template_name = 'workflow/mturk/workflow_form.html'
    success_url = reverse_lazy('workflow:feedback')

    def get_form_class(self):
        return self.form_classes.get(self.workflow.type)

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'item': self.item,
            'answer_start': timezone.now(),
            'workerId': self.request.GET.get('workerId'),
        })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'skip_done_button': True,
            'ab_group': self.ab_group,
        })
        return kwargs

    def quality_check(self):
        item_link_clicked, corroborating_link_clicked = \
            RedirectLinkClicked.objects.get_status(rater=self.rater,
                                                   item=self.item)
        quality_check_failed = not item_link_clicked
        if self.workflow.pk == Workflow.EVIDENCE_URLS_JUDGMENT:  # 3rd workflow
            if ItemURLs.objects.get_choices(self.item):  # have evidence links?
                quality_check_failed = quality_check_failed or \
                                       not corroborating_link_clicked

        if quality_check_failed:
            if not self.object.rater.probation:  # if that happened first time:
                self.object.rater.probation = True
                self.object.rater.save()
            else:  # if that happened second time:
                self.object.rater.disassociate_qualification()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.workflow = self.workflow
        self.object.rater = self.rater
        self.object.answer_end = timezone.now()
        self.object.save()

        self.quality_check()

        if self.request.is_ajax():
            return HttpResponse(status=200)
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        """Do some error checks and set self.item"""
        item_id = request.POST.get('item') or kwargs.get('pk') or 1
        try:
            self.object = LabelingAnswer.objects.get(rater=self.rater,
                                                     item__pk=item_id)
            self.item = Item.objects.get(pk=item_id)
            return HttpResponseRedirect(self.get_success_url())
        except LabelingAnswer.DoesNotExist:
            pass

        self.item = self.get_item()
        if not self.item:
            messages.error(request,
                           f'Item id {item_id} is missing or has already '
                           f'been labeled by rater id {self.rater.id}')
            return HttpResponseRedirect(reverse('workflow:error'))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.workflow.pk == Workflow.JOURNALIST_WORKFLOW:  # 4th workflow
            return self.get_url_with_params(reverse('workflow:auto-send'))
        success_url = super().get_success_url()
        return f'{success_url}&item={self.item.pk}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'journalist_workflow':
                self.workflow.pk == Workflow.JOURNALIST_WORKFLOW,
        })
        return context


@method_decorator(decorators, name='dispatch')
class FeedbackView(FeedbackMixin, RaterWorkflowMixin, BaseLastStepView):
    template_name = 'workflow/mturk/feedback.html'
    form_class = FeedbackForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.request.GET.get('item')
        answers = LabelingAnswer.objects.filter(rater=self.rater). \
            filter(item=item).get()
        context.update({
            'remove': {**context['remove'], 'your': answers.predict_remove},
            'reduce': {**context['reduce'], 'your': answers.predict_reduce},
            'inform': {**context['inform'], 'your': answers.predict_inform},
        })
        return context


@method_decorator(decorators, name='dispatch')
class MTurkAutoSendView(BaseLastStepView):
    template_name = 'workflow/mturk/mturk-auto-send.html'
    form_class = MTurkAutoSendForm


@method_decorator(decorators[2:], name='dispatch')
# Don't require login or rater to be present.
# Will create and log them in as part of .get()
class QualifyView(ForwardRedirectArguments, FormView):
    template_name = 'workflow/mturk/qualify.html'
    form_class = QualifyForm
    success_url = reverse_lazy('workflow:labelone')

    def get(self, request, *args, **kwargs):
        rater = self.get_rater()
        if not rater:
            self.template_name = 'workflow/mturk/qualifyPreview.html'
        return super().get(request, *args, **kwargs)

    def get_rater(self):
        worker_id = self.request.GET.get('workerId')
        if worker_id:
            rater, _ = Rater.objects.get_or_create(
                worker_id=worker_id,
                defaults={
                    'worker_id': worker_id,
                })
            user = authenticate(self.request, worker_id=worker_id)
            login(self.request, user)
            return rater
        elif self.request.user.is_superuser:
            return self.request.user.rater
        else:
            return None


@method_decorator(decorators, name='dispatch')
class LabelOneView(WorkflowFormView):
    template_name = 'workflow/mturk/labelone.html'
    success_url = reverse_lazy('workflow:quiz')

    def get_item(self):
        return super().get_item(item_id=1)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'skip_done_button': False,
        })
        return kwargs

    def quality_check(self):
        pass  # disable quality check on /labelone


@method_decorator(decorators, name='dispatch')
class QuizView(RedirectToNextMixin, FeedbackMixin, ForwardRedirectArguments,
               RaterWorkflowMixin, CreateView):
    template_name = 'workflow/mturk/quiz.html'
    form_class = QuizForm
    success_url = reverse_lazy('workflow:consent')

    def get_form_class(self):
        if self.workflow.type == 'EVIDENCE_URL_INPUT_WORKFLOW':
            return QuizFormWorkflow2
        return super().get_form_class()

    def get_answered_item(self):
        result = QuizAnswer.objects.\
            filter(Q(second_attempt=True) | Q(closed=True)).\
            get(rater=self.rater)
        return result

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.rater = self.rater
        self.object.save()
        form.save_m2m()

        if not self.object.is_test_passed:
            if not self.object.second_attempt:
                self.object.second_attempt = True
                form = QuizForm(instance=self.object)
                return self.form_invalid(form)
            else:
                self.object.closed = True
                self.object.save()
                return HttpResponseRedirect(self.get_fail_url())

        self.object.closed = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        label_form_class = WorkflowMixin.form_classes.get(self.workflow.type)
        item = Item.active.get_answered(self.rater).get(pk=1)
        instance = LabelingAnswer.objects.get(rater=self.rater, item=item)
        label_form = label_form_class(
            instance=instance, ab_group=self.rater.ab_group,
            initial={'item': item}
        )

        context.update({
            'rater': self.rater,
            'label_form': label_form,
            'item': item,
            'workflow': self.workflow,  # fixme: never used, remove?
            'remove': {**context['remove'], 'your': instance.predict_remove},
            'reduce': {**context['reduce'], 'your': instance.predict_reduce},
            'inform': {**context['inform'], 'your': instance.predict_inform},
        })
        return context


@method_decorator(decorators, name='dispatch')
class ConsentView(SaveAnswerMixin, ForwardRedirectArguments,
                  RaterWorkflowMixin, CreateView):
    template_name = 'workflow/mturk/consent.html'
    form_class = ConsentForm
    success_url = reverse_lazy('workflow:knowledge')

    def form_valid(self, form):
        super().form_valid(form)

        if not self.object.is_test_passed:
            return HttpResponseRedirect(self.get_fail_url())
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(decorators, name='dispatch')
class KnowledgeView(RedirectToNextMixin, SaveAnswerMixin,
                    ForwardRedirectArguments, RaterWorkflowMixin, CreateView):
    template_name = 'workflow/mturk/knowledge.html'
    form_class = KnowledgeForm
    success_url = reverse_lazy('workflow:demographics')

    def form_valid(self, form):
        super().form_valid(form)

        if not self.object.is_test_passed:
            return HttpResponseRedirect(self.get_fail_url())
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(decorators, name='dispatch')
class TestView(SaveAnswerMixin, RaterWorkflowMixin, CreateView):  # might need to change if use Mturnk
    template_name = 'workflow/mturk/test.html'
    form_class = TestForm
    #success_url = reverse_lazy('workflow:congratulations') # what happen after answer
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'correct_answers': ['Civil','Civil','Uncivil','Civil','Civil','Uncivil','Civil'],  #infomration of correct answer
        })
        return context

@method_decorator(decorators, name='dispatch')
class DemographicsView(RedirectToNextMixin, SaveAnswerMixin,
                       ForwardRedirectArguments, RaterWorkflowMixin,
                       CreateView):
    template_name = 'workflow/mturk/demographics.html'
    form_class = DemographicsForm
    success_url = reverse_lazy('workflow:congratulations')

    def form_valid(self, form):
        super().form_valid(form)

        # assign rater to a rater_group (e.g., "3B")

        # first, determine the group number,
        # based on political affiliation and workflow assigned to the user
        affiliation = self.object.get_political_lean()
        workflow = self.object.rater.workflow.type

        group_num = WORKFLOW_GROUPS[workflow][affiliation]

        if self.rater.rater_group:
            logging.error(f"At end of /demographics, rater already has a rater"
                          f" group {self.rater.rater_group}. Not reassigning.")
        else:
            rater_group = f'{group_num}{self.rater.ab_group}'
            self.rater.rater_group = rater_group
            self.rater.save()

            # do the assignment on mturk
            self.object.rater.associate_qualification()

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(decorators, name='dispatch')
class CongratulationsView(BaseLastStepView, RaterWorkflowMixin):
    template_name = 'workflow/mturk/congratulations.html'
    form_class = CongratulationsForm
    # don't need `success_url` here because we change `action` in template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'workgroup': self.rater.rater_group,
        })
        return context


@method_decorator(decorators, name='dispatch')
class ThankYouView(BaseLastStepView):
    template_name = 'workflow/mturk/thankyou.html'
    form_class = ThankYouForm
    # don't need `success_url` here because we change `action` in template
