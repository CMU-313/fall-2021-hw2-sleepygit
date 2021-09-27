from django.apps import apps
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.sources.classes import DocumentCreateWizardStep
from mayan.apps.views.http import URL

from .forms import ReviewerMultipleSelectionForm
from .models import Reviewer
from .permissions import permission_reviewer_attach


class DocumentCreateWizardStepReviewers(DocumentCreateWizardStep):
    form_class = ReviewerMultipleSelectionForm
    label = _('Select reviewers')
    name = 'reviewer_selection'
    number = 2

    @classmethod
    def condition(cls, wizard):
        Reviewer = apps.get_model(app_label='reviewers', model_name='Reviewer')
        return Reviewer.objects.exists()

    @classmethod
    def get_form_kwargs(self, wizard):
        return {
            'help_text': _('Reviewers to be attached.'),
            'model': Reviewer,
            'permission': permission_reviewer_attach,
            'user': wizard.request.user
        }

    @classmethod
    def done(cls, wizard):
        result = {}
        cleaned_data = wizard.get_cleaned_data_for_step(cls.name)
        if cleaned_data:
            result['reviewers'] = [
                force_text(s=reviewer.pk) for reviewer in cleaned_data['reviewers']
            ]

        return result

    @classmethod
    def step_post_upload_process(cls, document, querystring=None):
        Reviewer = apps.get_model(app_label='reviewers', model_name='Reviewer')

        reviewer_id_list = URL(query_string=querystring).args.getlist('reviewers')

        for reviewer in Reviewer.objects.filter(pk__in=reviewer_id_list):
            reviewer.documents.add(document)


DocumentCreateWizardStep.register(step=DocumentCreateWizardStepReviewers)
