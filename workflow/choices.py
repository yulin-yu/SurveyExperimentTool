from extended_choices import Choices

YES_NO_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)
JUDGMENT_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)

WORKFLOW_TYPE_CHOICES = Choices(
    ['WITHOUT_EVIDENCE_URL_WORKFLOW', 'without evidence url workflow',
     'without evidence url workflow'],
    ['EVIDENCE_URL_INPUT_WORKFLOW', 'evidence url input workflow',
     'evidence url input workflow'],
    ['EVIDENCE_URLS_JUDGMENT_WORKFLOW', 'evidence urls judgment workflow',
     'evidence urls judgment workflow'],
)

TAKE_ACTION_CHOICES = (
    ('Yes', 'Yes, one or more of these actions should be taken.'),
    ('No', 'No, none of these actions should be taken.'),
    ('Not enough info', "I don't have enough information to judge")
)


JUDGMENT_REMOVE_CHOICES = (
    (True, 'Yes, platforms should remove the item.'),
    (False, 'No, platforms should not remove the item.'),
)

JUDGMENT_REDUCE_CHOICES = (
    (True, 'Yes, if the item is not removed, platforms should reduce '
           'exposure to the item.'),
    (False, 'No, platforms should not reduce exposure to the item.'),
)

JUDGMENT_INFORM_CHOICES = (
    (True, 'Yes, if the item is not removed, platforms should inform users '
           'that it may be misleading.'),
    (False, 'No, platforms should not inform users that the item '
            'may be misleading.'),
)

JUDGMENT_MISLEADING_ITEM_CHOICES = (
    (None, ''),
    (1, '1 = not misleading at all'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7 = false or extremely misleading'),
    (0, "I don't have enough information to make a judgment")
)

JUDGMENT_HARM_CHOICES = (
    (None, ''),
    (1, '1 = No harm at all'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7 = Extremely harmful'),
)

WORKFLOW_GROUPS = {
    'WITHOUT_EVIDENCE_URL_WORKFLOW': {
        'Liberal': 1,
        'Moderate': 2,
        'Conservative': 3
    },
    'EVIDENCE_URL_INPUT_WORKFLOW': {
        'Liberal': 4,
        'Moderate': 5,
        'Conservative': 6
    },
    'EVIDENCE_URLS_JUDGMENT_WORKFLOW': {
        'Liberal': 7,
        'Moderate': 8,
        'Conservative': 9
    },
    # ...
}

Test_Select = (
    (None, ''),
    ('Uncivil', 'Uncivil: The comment criticizes other people or their ideas in insulting ways, argues that people who disagree with them should suffer, or tells them to stop expressing opinions.'),
    ('Civil', 'Civil: The comment is not uncivil – it takes a stance, even a strong one, without attacking people who disagree or arguing that they should stop talking.'),
)
