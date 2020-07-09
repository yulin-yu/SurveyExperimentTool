from functools import update_wrapper

from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from workflow.models import ReduceChoices, QuizAnswer, \
    JudgmentRequirementChoices, CorroboratingChoices, Item, Rater, \
    LabelingAnswer, ItemWorkflow, Workflow, Assignment, InformChoices, \
    RemoveChoices, Qualification, ItemURLs, ConsentAnswer, DemographicsAnswer,\
    KnowledgeAnswer, ItemAnswers, RedirectLinkClicked,TestAnswer
from workflow.services.mturk import mturk


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    change_list_template = 'workflow/admin.html'

@admin.register(TestAnswer)
class TestAnswer(admin.ModelAdmin):
    list_display = ("created_at",)
    readonly_fields = ("created_at", )

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'url', 'is_active', 'hits', 'category')
    actions = ['create_hits', 'set_item_urls', 'set_item_counts']

    def hits(self, obj: Item):
        hits = list(map(str, obj.itemworkflow_set.all()))
        return mark_safe('<br />'.join(hits))

    def create_hits(self, request, queryset):
        if 'apply' in request.POST:

            for item in queryset:
                for workflow in request.POST.getlist('workflows'):
                    urls = item.create_hits(workflow)
                    for url in urls:
                        messages.info(request, url)

            return HttpResponseRedirect(request.get_full_path())
        return render(request,
                      'admin/workflow/item/create_hits.html',
                      context={
                          'items': queryset,
                          'workflows': Workflow.objects.exclude(
                              pk=Workflow.JOURNALIST_WORKFLOW,
                          )
                      })

    def set_item_urls(self, request, queryset):
        for item in queryset:
            item.set_item_urls()
        return HttpResponseRedirect(request.get_full_path())

    def set_item_counts(self, request, queryset):
        for object in queryset:
            object.set_item_counts()
        messages.info(request, 'ItemAnswer entries were created.')
        return HttpResponseRedirect(request.get_full_path())

    def create_labeling_hits_for_workflow_3(self, request):
        created = False
        for item in Item.active.newly_ready():
            urls = item.create_hits(Workflow.EVIDENCE_URLS_JUDGMENT)
            created = True
            for url in urls:
                messages.info(request, url)
        if not created:
            messages.info(request,
                          "Any HITs weren't created (no newly ready items)")
        return redirect('admin:workflow_itemworkflow_changelist')

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        return [
            path('labeling-hits-for-workflow-3/',
                 wrap(self.create_labeling_hits_for_workflow_3),
                 name='labeling_hits_for_workflow_3'),
        ] + super().get_urls()

    create_hits.short_description = 'Create HITs'
    set_item_urls.short_description = 'Set Workflow 3 Item URLs'
    set_item_counts.short_description = 'Set Item Workflow Counts'


@admin.register(ItemWorkflow)
class ItemWorkflowAdmin(admin.ModelAdmin):
    list_display = (
        'hit_id', 'item', 'qualification', 'workflow',
        # 'workflow__qualification',
        'created_at'
    )


@admin.register(ItemURLs)
class ItemURLsAdmin(admin.ModelAdmin):
    list_display = ('item', 'prev_urls')


@admin.register(ItemAnswers)
class ItemAnswersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'item', 'workflow', 'inform_count', 'reduce_count',
                    'remove_count', 'total_simulated_answers', 'created_at')


@admin.register(ReduceChoices)
class ReduceNumberOfPeopleChoicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_correct')


@admin.register(InformChoices)
class WarnPeopleChoicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_correct')


@admin.register(RemoveChoices)
class RemoveChoicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_correct')


@admin.register(JudgmentRequirementChoices)
class JudgmentRequirementChoicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_correct')


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['rater_id', 'workflow', 'is_test_passed']

    def rater_email(self, obj: QuizAnswer):
        return obj.rater.worker_id

    def workflow(self, obj: QuizAnswer):
        return obj.rater.workflow.get_type_display()

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        return [
            path('qualification-hits/',
                 wrap(self.create_qualification_hit),
                 name='qualification_hits'),
        ] + super().get_urls()

    def create_qualification_hit(self, request):
        already_qualified_id = \
            Qualification.objects.get(name='CSMR-Labeling-qualification-complete').mturk_id
        hit = mturk.register_hit('qualification', reverse('workflow:qualify'),
                                 extra_qualifications=[
                                     {
                                         "QualificationTypeId": already_qualified_id,
                                         "Comparator": "DoesNotExist",
                                         'ActionsGuarded': 'PreviewAndAccept'
                                     }
                                 ],
                                 )
        hit_type_id = hit['HITTypeId']
        url = f'{settings.MTURK_ENDPOINT}/mturk/preview?groupId={hit_type_id}'
        messages.info(request, url)
        return HttpResponseRedirect(reverse(
            'admin:workflow_quizanswer_changelist'))


@admin.register(LabelingAnswer)
class LabelingAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'rater', 'item', 'workflow',
        'inform', 'reduce', 'remove',
    )

    def inform(self, obj):
        return obj.judgment_inform

    def reduce(self, obj):
        return obj.judgment_reduce

    def remove(self, obj):
        return obj.judgment_remove

    inform.short_description = 'inform'
    inform.boolean = True

    reduce.short_description = 'reduce'
    reduce.boolean = True

    remove.short_description = 'remove'
    remove.boolean = True


@admin.register(CorroboratingChoices)
class CorroboratingChoicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_correct')


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'mturk_id')


admin.site.register(Rater)
admin.site.register(ConsentAnswer)
admin.site.register(KnowledgeAnswer)
admin.site.register(DemographicsAnswer)
admin.site.register(Assignment)
admin.site.register(RedirectLinkClicked)
