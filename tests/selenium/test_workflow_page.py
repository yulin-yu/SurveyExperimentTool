from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from selenium.common.exceptions import NoSuchElementException

from workflow.models import Rater, Workflow, Item, LabelingAnswer
from workflow.alerts import INVALID_WORKFLOW_ALERTS, WORKFLOW_DONE_ALERTS
from tests.selenium.base import SeleniumBaseRemoteTest
from workflow.choices import WORKFLOW_TYPE_CHOICES


SUCCESS_ALERTS_XPATH = '//div[@class="alert alert-success alert-dismissible fade show"]'
WARNING_ALERTS_XPATH = '//div[@class="alert alert-warning alert-dismissible fade show"]'
WORKFLOW_NAME = 'workflow1'
WORKFLOW_TYPE = WORKFLOW_TYPE_CHOICES.WITHOUT_EVIDENCE_URL_WORKFLOW


class WorkflowPageWithUnExistedWorkflowTest(SeleniumBaseRemoteTest):

    def test_answer(self):
        item = Item.objects.create(url='www.test.com', category='test_category', is_active=True)
        workflow = None
        for x in range(1, 10):
            workflow = Workflow.objects.create(
                api_id=x,
                name='invalid_workflow',
                instruction=x,
                judgment_enough_information=x,
                judgment_misleading_item=x,
                judgment_remove_reduce_inform_head=x,
                judgment_remove=x,
                judgment_reduce=x,
                judgment_inform=x,
                prediction=x,
                type='invalid_type')
        rater = Rater.objects.create(
            email='test10@test.com',
            api_id='test_judgment10',
            age=10,
            gender='m',
            location='Kiev',
            workflow=workflow)
        previous_rater = Rater.objects.create(
            email='test_judgment_previous10@test.com',
            api_id='test_judgment_previous10',
            age=10,
            gender='m',
            location='Kiev',
            workflow=workflow)
        answer_start = datetime.now()
        answer_end = datetime.now()
        answer = LabelingAnswer.objects.create(
            id=9,
            rater=previous_rater,
            item=item,
            workflow=workflow,
            answer_start=answer_start,
            answer_end=answer_end,
            evidence_url='https//test.evidence.com'
        )

        selenium = self.selenium
        selenium.get(self.live_server_url)

        session = self.client.session
        session['rater_id'] = 'test_judgment10'
        session.save()
        selenium.add_cookie({'name': 'sessionid', 'value': session._SessionBase__session_key,
                             'secure': False, 'path': '/'})
        selenium.get(f'{self.live_server_url}/workflow_form')
        alerts = [alert.text.replace('\n×', '') for alert in selenium.find_elements_by_xpath(WARNING_ALERTS_XPATH)]
        self.assertEqual(alerts, INVALID_WORKFLOW_ALERTS)
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_id_rater_answer_judgment_0_1')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_id_evidence_url_0_1')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_rater_answer_predict_a')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_rater_answer_predict_b')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_rater_answer_predict_c')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('submit')

        with self.assertRaises(ObjectDoesNotExist):
            LabelingAnswer.objects.exclude(id=answer.id).get(rater=rater, item=item, workflow=workflow)
        self.assertEqual(LabelingAnswer.objects.all().count(), 1)


class WorkflowPageWithUnActiveItemTest(SeleniumBaseRemoteTest):

    def test_answer(self):
        item = Item.objects.create(url='www.test.com', category='test_category', is_active=False)
        workflow = None
        for x in range(1, 10):
            workflow = Workflow.objects.create(
                api_id=x,
                name=WORKFLOW_NAME,
                instruction=x,
                judgment_enough_information=x,
                judgment_misleading_item=x,
                judgment_remove_reduce_inform_head=x,
                judgment_remove=x,
                judgment_reduce=x,
                judgment_inform=x,
                prediction=x,
                type=WORKFLOW_TYPE)
        rater = Rater.objects.create(
            email='test10@test.com',
            api_id='test_judgment10',
            age=10,
            gender='m',
            location='Kiev',
            workflow=workflow)
        previous_rater = Rater.objects.create(
            email='test_judgment_previous10@test.com',
            api_id='test_judgment_previous10',
            age=10,
            gender='m',
            location='Kiev',
            workflow=workflow)
        answer_start = datetime.now()
        answer_end = datetime.now()
        answer = LabelingAnswer.objects.create(
            id=9,
            rater=previous_rater,
            item=item,
            workflow=workflow,
            answer_start=answer_start,
            answer_end=answer_end,
            evidence_url='https//test.evidence.com'
        )

        selenium = self.selenium
        selenium.get(self.live_server_url)

        session = self.client.session
        session['rater_id'] = 'test_judgment10'
        session.save()
        selenium.add_cookie({'name': 'sessionid', 'value': session._SessionBase__session_key,
                             'secure': False, 'path': '/'})
        selenium.get(f'{self.live_server_url}/workflow_form')
        alerts = [alert.text.replace('\n×', '') for alert in selenium.find_elements_by_xpath(SUCCESS_ALERTS_XPATH)]
        self.assertEqual(alerts, WORKFLOW_DONE_ALERTS)
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_id_rater_answer_judgment_0_1')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_rater_answer_predict_a')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_rater_answer_predict_b')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('id_rater_answer_predict_c')
        with self.assertRaises(NoSuchElementException):
            selenium.find_element_by_id('submit')

        with self.assertRaises(ObjectDoesNotExist):
            LabelingAnswer.objects.exclude(id=answer.id).get(rater=rater, item=item, workflow=workflow)
        self.assertEqual(LabelingAnswer.objects.all().count(), 1)

