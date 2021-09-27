import logging

from django.shortcuts import reverse
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.classes import ModelQueryFields
from mayan.apps.documents.models import Document
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    MultipleObjectFormActionView, MultipleObjectConfirmActionView,
    SingleObjectCreateView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import ReviewerMultipleSelectionForm
from .icons import icon_menu_tags, icon_document_tag_remove_submit
from .links import link_document_reviewer_multiple_attach, link_reviewer_create
from .models import DocumentReviewer, Reviewer
from .permissions import (
    permission_reviewer_attach, permission_reviewer_create, permission_reviewer_remove,
    permission_reviewer_view, permission_reviewer_delete, permission_reviewer_edit,
)

logger = logging.getLogger(name=__name__)


class ReviewerAttachActionView(MultipleObjectFormActionView):
    form_class = ReviewerMultipleSelectionForm
    object_permission = permission_reviewer_attach
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _(
        'Reviewers attached to document "%(object)s" successfully.'
    )
    success_message_singular = _(
        'Reviewers attached to %(count)d document successfully.'
    )
    success_message_plural = _(
        'Reviewers attached to %(count)d documents successfully.'
    )
    title_single = _('Attach reviwers to document: %(object)s')
    title_singular = _('Attach reviewers to %(count)d document.')
    title_plural = _('Attach reviewers to %(count)d documents.')

    def get_extra_context(self):
        context = {
            'submit_label': _('Attach'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _('Reviewers to be attached.'),
            'permission': permission_reviewer_attach,
            'queryset': Reviewer.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': Reviewer.objects.exclude(
                        pk__in=self.object_list.first().reviewers.all()
                    )
                }
            )

        return kwargs

    def get_post_action_redirect(self):
        if self.object_list.count() == 1:
            return reverse(
                viewname='reviewers:document_reviewer_list', kwargs={
                    'document_id': self.object_list.first().pk
                }
            )
        else:
            return super().get_post_action_redirect()

    def object_action(self, form, instance):
        for reviewer in form.cleaned_data['reviewers']:
            AccessControlList.objects.check_access(
                obj=reviewer, permissions=(permission_reviewer_attach,),
                user=self.request.user
            )

            reviewer._event_actor = self.request.user
            reviewer.attach_to(document=instance)

class ReviewerAddActionView(MultipleObjectFormActionView):
    form_class = ReviewerMultipleSelectionForm
    object_permission = permission_reviewer_attach
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _(
        'Reviewers added to application document "%(object)s" successfully.'
    )
    success_message_singular = _(
        'Reviewers added to %(count)d application document successfully.'
    )
    success_message_plural = _(
        'Reviewers added to %(count)d application documents successfully.'
    )
    title_single = _('Add reviewers to application document: %(object)s')
    title_singular = _('Add reviewers to %(count)d application document.')
    title_plural = _('Add reviewers to %(count)d application documents.')

    def get_extra_context(self):
        context = {
            'submit_label': _('Add'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _('Reviewers to be added.'),
            'permission': permission_reviewer_attach,
            'queryset': Reviewer.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': Reviewer.objects.exclude(
                        pk__in=self.object_list.first().reviewer.all()
                    )
                }
            )

        return kwargs

    def get_post_action_redirect(self):
        if self.object_list.count() == 1:
            return reverse(
                viewname='reviewers:document_reviewer_list', kwargs={
                    'document_id': self.object_list.first().pk
                }
            )
        else:
            return super().get_post_action_redirect()

    def object_action(self, form, instance):
        for reviewer in form.cleaned_data['reviewers']:
            AccessControlList.objects.check_access(
                obj=reviewer, permissions=(permission_reviewer_attach,),
                user=self.request.user
            )

            reviewer._event_actor = self.request.user
            reviewer.attach_to(document=instance)


class ReviewerCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create reviewer')}
    fields = ('label', 'color')
    model = Reviewer
    post_action_redirect = reverse_lazy(viewname='reviewer:reviewer_list')
    view_permission = permission_reviewer_create

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ReviewerDeleteActionView(MultipleObjectConfirmActionView):
    error_message = _('Error deleting reviewer "%(instance)s"; %(exception)s')
    model = Reviewer
    object_permission = permission_reviewer_delete
    pk_url_kwarg = 'reviewer_id'
    post_action_redirect = reverse_lazy(viewname='reviewers:reviewer_list')
    success_message_single = _('Reviewer "%(object)s" deleted successfully.')
    success_message_singular = _('%(count)d reviewer deleted successfully.')
    success_message_plural = _('%(count)d reviewers deleted successfully.')
    title_single = _('Delete reviewer: %(object)s.')
    title_singular = _('Delete the %(count)d selected reviewer.')
    title_plural = _('Delete the %(count)d selected reviewers.')

    def get_extra_context(self):
        context = {
            'delete_view': True,
            'message': _('Will be removed from all application documents.'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def object_action(self, instance, form=None):
        instance.delete()


class ReviewerEditView(SingleObjectEditView):
    fields = ('label', 'color')
    model = Reviewer
    object_permission = permission_reviewer_edit
    pk_url_kwarg = 'reviewer_id'
    post_action_redirect = reverse_lazy(viewname='reviewers:reviewer_list')

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit reviewer: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ReviewerListView(SingleObjectListView):
    object_permission = permission_reviewer_view
    reviewer_model = Reviewer

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_menu_tags,
            'no_results_main_link': link_reviewer_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Reviewers are users that can be added or '
                'removed from application documents.'
            ),
            'no_results_title': _('No reviewers available'),
            'title': _('Reviewers'),
        }

    def get_source_queryset(self):
        queryset = ModelQueryFields.get(model=self.reviewer_model).get_queryset()
        return queryset.filter(pk__in=self.get_reviewer_queryset())

    def get_reviewer_queryset(self):
        return Reviewer.objects.all()


class ReviewerDocumentListView(ExternalObjectViewMixin, DocumentListView):
    external_object_class = Reviewer
    external_object_permission = permission_reviewer_view
    external_object_pk_url_kwarg = 'reviewer_id'

    def get_document_queryset(self):
        return Document.valid.filter(
            pk__in=self.get_reviewer().get_documents(
                permission=permission_reviewer_view, user=self.request.user
            ).values('pk')
        )

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'object': self.get_reviewer(),
                'title': _('Application documents with the reviewer: %s') % self.get_reviewer(),
            }
        )
        return context

    def get_reviewer(self):
        return self.external_object


class DocumentReviewerListView(ExternalObjectViewMixin, ReviewerListView):
    external_object_permission = permission_reviewer_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid
    reviewer_model = DocumentReviewer

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'hide_link': True,
                'no_results_main_link': link_document_reviewer_multiple_attach.resolve(
                    context=RequestContext(
                        self.request, {'object': self.external_object}
                    )
                ),
                'no_results_title': _('Application document has no reviewers added'),
                'object': self.external_object,
                'title': _(
                    'Reviewers for application document: %s'
                ) % self.external_object,
            }
        )
        return context

    def get_reviewer_queryset(self):
        return self.external_object.get_reviewers(
            permission=permission_reviewer_view, user=self.request.user
        )


class ReviewerRemoveActionView(MultipleObjectFormActionView):
    form_class = ReviewerMultipleSelectionForm
    object_permission = permission_reviewer_remove
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _(
        'Reviewers removed from application document "%(object)s" successfully.'
    )
    success_message_singular = _(
        'Reviewers removed from %(count)d application document successfully.'
    )
    success_message_plural = _(
        'Reviewers removed from %(count)d application documents successfully.'
    )
    title_single = _('Remove reviewers from application document: %(object)s')
    title_singular = _('Remove reviewers from %(count)d application document.')
    title_plural = _('Remove reviewers from %(count)d application documents.')

    def get_extra_context(self):
        context = {
            'submit_icon': icon_document_tag_remove_submit,
            'submit_label': _('Remove'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _('Reviewers to be removed.'),
            'permission': permission_reviewer_remove,
            'queryset': Reviewer.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': self.object_list.first().reviewers.all()
                }
            )

        return kwargs

    def get_post_action_redirect(self):
        if self.object_list.count() == 1:
            return reverse(
                viewname='reviewers:document_reviewer_list', kwargs={
                    'document_id': self.object_list.first().pk
                }
            )
        else:
            return super().get_post_action_redirect()

    def object_action(self, form, instance):
        for reviewer in form.cleaned_data['reviewers']:
            AccessControlList.objects.check_access(
                obj=reviewer, permissions=(permission_reviewer_remove,),
                user=self.request.user
            )

            reviewer._event_actor = self.request.user
            reviewer.remove_from(document=instance)
