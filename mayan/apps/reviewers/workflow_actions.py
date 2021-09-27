import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction

from .models import Reviewer
from .permissions import permission_reviewer_attach, permission_reviewer_remove

__all__ = ('AttachReviewerAction', 'RemoveReviewerAction')
logger = logging.getLogger(name=__name__)


class AttachReviewerAction(WorkflowAction):
    fields = {
        'reviewers': {
            'label': _('Reviewers'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Reviewers to attach to the document'),
                'queryset': Reviewer.objects.none(), 'required': False
            }
        },
    }
    label = _('Attach reviewer')
    media = {
        'js': ('tags/js/tags_form.js',)
    }
    widgets = {
        'reviewers': {
            'class': 'mayan.apps.reviewers.widgets.ReviewerFormWidget', 'kwargs': {
                'attrs': {'class': 'select2-tags'},
            }
        }
    }
    permission = permission_reviewer_attach

    def execute(self, context):
        for reviewer in self.get_reviewers():
            reviewer.attach_to(document=context['document'])

    def get_form_schema(self, **kwargs):
        result = super().get_form_schema(**kwargs)

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.permission, queryset=Reviewer.objects.all(),
            user=kwargs['request'].user
        )

        result['fields']['reviewers']['kwargs']['queryset'] = queryset

        return result

    def get_reviewers(self):
        return Reviewer.objects.filter(pk__in=self.form_data.get('reviewers', ()))


class RemoveReviewerAction(AttachReviewerAction):
    fields = {
        'reviewers': {
            'label': _('Reviewers'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Reviewers to remove from the document'),
                'queryset': Reviewer.objects.none(), 'required': False
            }
        },
    }
    label = _('Remove reviewer')
    permission = permission_reviewer_remove

    def execute(self, context):
        for reviewer in self.get_reviewers():
            reviewer.remove_from(document=context['document'])
