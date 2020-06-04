import logging

import boto3
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse_lazy

CONFIGURATION_FILE_PATH = 'input_files/mturk_configuration.json'
QUESTION_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
  <ExternalURL>{}</ExternalURL>
  <FrameHeight>0</FrameHeight>
</ExternalQuestion>
"""


class MTurkConnection:
    def __init__(self):
        endpoint_url = settings.MTURK_ENDPOINT
        self.client = boto3.client(
            'mturk',
            endpoint_url=endpoint_url,
            region_name=settings.MTURK_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.configuration = None

    def create_qualification(self, configuration):
        """
        Configuration required can be found here:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_qualification_type
        :param configuration:
        :return: MTurk ID for the qualification type
        """
        try:
            existing = self.client.list_qualification_types(
                Query=configuration['Name'],
                MustBeRequestable=False,
            )
            if existing['NumResults'] > 0:
                return existing['QualificationTypes'][0]['QualificationTypeId']
            else:
                response = \
                    self.client.create_qualification_type(**configuration)
                return response['QualificationType']['QualificationTypeId']
        except Exception as e:
            logging.error(f"Failed to create or locate credential "
                          f"{configuration['Name']}. Error message {e}.")

    def associate_qualification(self, worker_id, qualification_type_id,
                                integer_value=1):
        try:
            response = self.client.associate_qualification_with_worker(
                QualificationTypeId=qualification_type_id,
                WorkerId=worker_id,
                IntegerValue=integer_value
            )
            return response
        except Exception as e:
            logging.error(f'failed to associate qualification with worker. '
                          f'Error message:\n{e}')

    def disassociate_qualification(self, worker_id, qualification_type_id):
        reason = \
            'We have revoked your qualification for the CSMR labeling tasks ' \
            'for quality control reasons. You will still be paid for the ' \
            'HITs you completed. If you think that there may be a bug in ' \
            'our quality control monitoring, please send us an email and ' \
            'we will investigate whether to reinstate your qualification.'

        try:
            mturk.client.disassociate_qualification_from_worker(
                WorkerId=worker_id,
                QualificationTypeId=qualification_type_id,
                Reason=reason,
            )
        except Exception as e:
            logging.error(f'failed to disassociate qualification from worker. '
                          f'Error message:\n{e}')

    def register_hit(self, hit_name, url, extra_qualifications=None,
                     configuration_overrides={},
                     title=None):

        if not url.startswith('https'):
            site = Site.objects.get_current()
            url = 'https://' + site.domain + url
        self._load_configuration()
        configuration = self.configuration[hit_name]
        for k in configuration_overrides:
            configuration[k] = configuration_overrides[k]
        title = title or configuration.get('Title')

        # check if this URL not already registered;
        # if so, add more assignments to existing
        existing_hit = None
        if hit_name == 'labeling':
            # it's a labeling HIT,
            # so see if we have one (for this worker group) with this url
            #   embedded in its Question
            type_id = extra_qualifications[0]['QualificationTypeId']
            res = self.client.\
                list_hits_for_qualification_type(QualificationTypeId=type_id)
            for hit in res['HITs']:
                if url in hit['Question']:
                    existing_hit = hit
        # else:
        #     # it's a qualification HIT, so see if we have one with that title
        #     res = self.client.list_hits()
        #     for hit in res['HITs']:
        #         if title  == hit['Title']:
        #             existing_hit = hit

        if existing_hit:
            # allow more workers to do this HIT
            try:
                self.client.create_additional_assignments_for_hit(
                    HITId=hit['HITId'],
                    NumberOfAdditionalAssignments=configuration.get('MaxAssignments'))
            except Exception as e:
                logging.error(e)
            return existing_hit

        else:
            #  post it for the first time
            qualifications = configuration.get('QualificationRequirements')
            if extra_qualifications:
                qualifications += extra_qualifications
            hit = self.client.create_hit(
                Title= title,
                Description=configuration.get('Description'),
                Keywords=configuration.get('Keywords'),
                Reward=configuration.get('Reward'),
                MaxAssignments=configuration.get('MaxAssignments'),
                LifetimeInSeconds=configuration.get('LifetimeInSeconds'),
                AssignmentDurationInSeconds=configuration.get(
                    'AssignmentDurationInSeconds'),
                AutoApprovalDelayInSeconds=configuration.get(
                    'AutoApprovalDelayInSeconds'),
                QualificationRequirements=qualifications,
                Question=QUESTION_TEMPLATE.format(url),
            )
            return hit['HIT']

    def _load_configuration(self):
        self.configuration = {
            "qualification": {
                "Title": "Qualification for News Assessment",
                'test_Title': "Test task; please do not take this HIT",
                "test_Description":
                    'This is a test task; we are having tech difficulties'
                    'that did not appear in the sandbox, so we need to run a test here.'
                    'Please check back later. Thanks.',
                "Description":
                    'This task is a qualification step that unlocks many more '
                    'HITs for assessing news articles, as part of a research '
                    'project at the University of Michigan Center for '
                    'Social Media Responsibility. We will start by asking you '
                    'to do one sample task, reading a news article and '
                    'answering a series of questions about how you think '
                    'social media and search engines, like Google, should '
                    'treat it . After that, we will ask you general questions '
                    'about politics and about you. This task will qualify you '
                    'for one of our labeler groups, 1A-9B and unlock the HITS '
                    'titled "Is this news item misleading?"',
                "Keywords": "survey, opinion, judgement, politics",
                "Reward": "1",
                "MaxAssignments": 18,
                "LifetimeInSeconds": 172800,  # 2 days
                "AssignmentDurationInSeconds": 60*60, # 60 minutes
                "AutoApprovalDelayInSeconds": 14400, # 4 hours
                "QualificationRequirements": [
                    {
                        "QualificationTypeId": "00000000000000000071",
                        "Comparator": "EqualTo",
                        "LocaleValues": [
                            {
                                "Country": "US"
                            }
                        ],
                        'ActionsGuarded': 'PreviewAndAccept'
                        # "RequiredToPreview": True
                    }
                ]
            },
            "labeling": {
                # "Title": "Is this news item misleading?",
                "Description":
                    'Assess whether news articles are misleading. '
                    'To qualify for these tasks, search for the paid HIT '
                    '"Qualification for News Assessment" from requester '
                    '"CSMR". That will qualify you for one of our labeler '
                    'groups, 1A-9B. '
                    'You may complete this HIT multiple times if it is available.',
                "Keywords": "text, labeling",
                "Reward": "0.0",
                "MaxAssignments": 9,
                "LifetimeInSeconds": 172800,
                "AssignmentDurationInSeconds": 2*60*60, # 120 minutes
                "AutoApprovalDelayInSeconds": 14400,
                "QualificationRequirements": [
                    {
                        "QualificationTypeId": "00000000000000000071",
                        "Comparator": "EqualTo",
                        "LocaleValues": [
                            {
                                "Country": "US"
                            }
                        ],
                        'ActionsGuarded': 'PreviewAndAccept'
                        # "RequiredToPreview": True
                    }
                ]
            }
        }

    def accept_assignment(self, assignment_id, requester_feedback,
                          override_rejection):
        return self.client.approve_assignment(
            AssignmentId=assignment_id,
            RequesterFeedback=requester_feedback,
            OverrideRejection=override_rejection,
        )


mturk = MTurkConnection()
