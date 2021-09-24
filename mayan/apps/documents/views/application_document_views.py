from django.utils.translation import ugettext_lazy as _

from ..icons import icon_document_list
from ..models.document_models import Document

from .document_views import DocumentListView

__all__ = ('ApplicationDocumentListView',)


class ApplicationDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return Document.valid.all()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_document_list,
                'no_results_text': _(
                    'This view will list the application documents created '
                    'in the system.'
                ),
                'no_results_title': _(
                    'There are no recently created application documents.'
                ),
                'title': _('Application Documents'),
            }
        )
        return context
