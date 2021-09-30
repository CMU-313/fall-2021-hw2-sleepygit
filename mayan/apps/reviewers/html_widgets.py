from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string

from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .permissions import permission_reviewer_view


class DocumentReviewerWidget(SourceColumnWidget):
    """
    A reviewer widget that displays the reviewers for the given document.
    """
    template_name = 'reviewers/document_reviewers_widget.html'

    def get_extra_context(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.value,
                permissions=(permission_reviewer_view,),
                user=self.request.user
            )
        except PermissionDenied:
<<<<<<< HEAD
            queryset = self.value.reviewers.none()
=======
            queryset = self.value.reviewer.none()
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
        else:
            queryset = self.value.get_reviewers(
                permission=permission_reviewer_view,
                user=self.request.user
            )

        return {'reviewers': queryset}


def widget_single_reviewer(reviewer):
    return render_to_string(
        template_name='reviewers/reviewer_widget.html', context={'reviewer': reviewer}
    )
