from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import FilteredSelectionForm

from .widgets import ReviewerFormWidget


class ReviewerMultipleSelectionForm(FilteredSelectionForm):
    class Media:
        js = ('reviewers/js/reviewers_form.js',)

    class Meta:
        allow_multiple = True
        field_name = 'reviewers'
        label = _('Reviewers')
        required = False
        widget_class = ReviewerFormWidget
        widget_attributes = {'class': 'select2-reviewers'}