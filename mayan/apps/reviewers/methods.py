from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def method_document_get_reviewers(self, permission, user):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentReviewer = apps.get_model(app_label='reviewers', model_name='DocumentReviewer')

    return AccessControlList.objects.restrict_queryset(
        permission=permission,
        queryset=DocumentReviewer.objects.filter(documents=self), user=user
    )


method_document_get_reviewers.help_text = _(
    'Return the reviewers attached to the document.'
)
method_document_get_reviewers.short_description = _('get_reviewers()')
