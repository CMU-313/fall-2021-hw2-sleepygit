from django.apps import apps
from django.db.models.signals import m2m_changed, pre_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import (
    ModelCopy, ModelFieldRelated, ModelQueryFields
)
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_secondary
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_reviewer_attached, event_reviewer_edited, event_reviewer_removed
)
from .handlers import handler_index_document, handler_reviewer_pre_delete
from .html_widgets import DocumentReviewerWidget
from .links import (
    link_document_reviewer_list, link_document_multiple_reviewer_multiple_attach,
    link_document_multiple_reviewer_multiple_remove,
    link_document_reviewer_multiple_remove, link_document_reviewer_multiple_attach, link_reviewer_create,
    link_reviewer_delete, link_reviewer_delete, link_reviewer_edit, link_reviewer_edit, link_reviewer_list, 
    link_reviewer_create, link_reviewer_list, link_reviewer_multiple_delete, link_reviewer_document_list,
    link_document_multiple_reviewer_multiple_add, 
    link_document_multiple_reviewer_multiple_remove
)
from .menus import menu_reviewers, menu_reviewers
from .methods import method_document_get_reviewers
from .permissions import (
    permission_reviewer_attach, permission_reviewer_delete, permission_reviewer_edit,
    permission_reviewer_remove, permission_reviewer_view
)


class ReviewersApp(MayanAppConfig):
    app_namespace = 'reviewers'
    app_url = 'reviewers'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.reviewers'
    verbose_name = _('Reviewers')

    def ready(self):
        super().ready()
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentFileSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentFileSearchResult'
        )
        DocumentFilePageSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentFilePageSearchResult'
        )
        DocumentVersionSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentVersionSearchResult'
        )
        DocumentVersionPageSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentVersionPageSearchResult'
        )

        DocumentReviewer = self.get_model(model_name='DocumentReviewer')
        Reviewer = self.get_model(model_name='Reviewer')

        Document.add_to_class(name='get_reviewers', value=method_document_get_reviewers)

        EventModelRegistry.register(model=Reviewer)

        ModelCopy(
            model=Reviewer, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'color', 'documents',
            ),
        )

        ModelEventType.register(
            model=Reviewer, event_types=(
                event_reviewer_attached, event_reviewer_edited, event_reviewer_removed
            )
        )

        ModelFieldRelated(model=Document, name='reviewers__label')
        ModelFieldRelated(model=Document, name='reviewers__color')

        ModelPermission.register(
            model=Document, permissions=(
                permission_reviewer_attach, permission_reviewer_remove,
                permission_reviewer_view
            )
        )

        ModelPermission.register(
            model=Reviewer, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_reviewer_attach,
                permission_reviewer_delete, permission_reviewer_edit,
                permission_reviewer_remove, permission_reviewer_view,
            )
        )

        model_query_fields_document = ModelQueryFields.get(model=Document)
        model_query_fields_document.add_prefetch_related_field(field_name='reviewers')

        model_query_fields_reviewer = ModelQueryFields.get(model=Reviewer)
        model_query_fields_reviewer.add_prefetch_related_field(field_name='documents')

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DocumentReviewer
        )

        SourceColumn(
            label=_('Reviewers'), source=Document, widget=DocumentReviewerWidget
        )

        SourceColumn(
            attribute='document', label=_('Reviewers'),
            source=DocumentFileSearchResult, widget=DocumentReviewerWidget
        )
        SourceColumn(
            attribute='document_file__document', label=_('Reviewers'),
            source=DocumentFilePageSearchResult, widget=DocumentReviewerWidget
        )

        SourceColumn(
            attribute='document', label=_('Reviewers'),
            source=DocumentVersionSearchResult, widget=DocumentReviewerWidget
        )
        SourceColumn(
            attribute='document_version__document', label=_('Reviewers'),
            source=DocumentVersionPageSearchResult, widget=DocumentReviewerWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Reviewer
        )
        SourceColumn(
            attribute='get_preview_widget', include_label=True, source=Reviewer
        )
        source_column_reviewer_document_count = SourceColumn(
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'), source=Reviewer
        )
        source_column_reviewer_document_count.add_exclude(source=DocumentReviewer)

        menu_facet.bind_links(
            links=(link_document_reviewer_list,), sources=(Document,)
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_reviewer_document_list,
            ), sources=(Reviewer,)
        )

        menu_reviewers.bind_links(
            links=(
                link_reviewer_list, link_reviewer_create
            )
        )

        menu_main.bind_links(links=(menu_reviewers,), position=98)

        menu_multi_item.bind_links(
            links=(
                link_document_multiple_reviewer_multiple_attach,
                link_document_multiple_reviewer_multiple_remove,
                link_document_multiple_reviewer_multiple_add,
                link_document_multiple_reviewer_multiple_remove
            ),
            sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(link_reviewer_multiple_delete,), sources=(Reviewer,)
        )
        # menu_object.bind_links(
        #     links=(
        #         link_reviewer_edit, link_reviewer_delete
        #     ),
        #     sources=(Reviewer,)
        # )
        menu_object.bind_links(
            links=(
                link_reviewer_edit, link_reviewer_delete
            ),
            sources=(Reviewer,)
        )
        menu_secondary.bind_links(
            links=(link_document_reviewer_multiple_attach, link_document_reviewer_multiple_remove),
            sources=(
                'reviewers:reviewer_attach', 'reviewers:document_reviewer_list',
                'reviewers:single_document_multiple_reviewer_remove'
            )
        )

        # Index update

        m2m_changed.connect(
            dispatch_uid='reviewers_handler_index_document',
            receiver=handler_index_document,
            sender=Reviewer.documents.through
        )

        pre_delete.connect(
            dispatch_uid='reviewers_handler_reviewer_pre_delete',
            receiver=handler_reviewer_pre_delete,
            sender=Reviewer
        )
