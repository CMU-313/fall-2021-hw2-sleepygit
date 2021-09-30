from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
<<<<<<< HEAD
    icon_document_reviewer_multiple_attach, icon_document_reviewer_multiple_remove,
    icon_document_reviewer_list, icon_reviewer_create, icon_reviewer_delete,
    icon_reviewer_document_list, icon_reviewer_edit, icon_reviewer_list
=======
    icon_document_tag_multiple_attach, icon_document_tag_multiple_remove,
    icon_document_tag_list, icon_tag_create, icon_tag_delete,
    icon_tag_document_list, icon_tag_edit, icon_tag_list
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
)
from .permissions import (
    permission_reviewer_attach, permission_reviewer_create, permission_reviewer_delete,
    permission_reviewer_edit, permission_reviewer_remove, permission_reviewer_view
)


link_document_multiple_reviewer_multiple_attach = Link(
<<<<<<< HEAD
    icon=icon_document_reviewer_multiple_attach, text=_('Attach reviewers'),
    view='reviewers:multiple_documents_reviewer_attach'
)
link_document_multiple_reviewer_multiple_add = Link(
    icon=icon_document_reviewer_multiple_attach, text=_('Add reviewers'),
    view='reviewers:multiple_documents_reviewer_add'
)
link_document_multiple_reviewer_multiple_remove = Link(
    icon=icon_document_reviewer_multiple_remove, text=_('Remove reviewer'),
    view='reviewers:multiple_documents_selection_reviewer_remove'
)
link_document_multiple_reviewer_multiple_remove = Link(
    icon=icon_document_reviewer_multiple_remove, text=_('Remove reviewer'),
    view='reviewers:multiple_documents_selection_reviewer_remove'
)
link_document_reviewer_list = Link(
    args='resolved_object.pk', icon=icon_document_reviewer_list,
=======
    icon=icon_document_tag_multiple_attach, text=_('Attach reviewers'),
    view='reviewers:multiple_documents_tag_attach'
)
link_document_multiple_reviewer_multiple_add = Link(
    icon=icon_document_tag_multiple_attach, text=_('Add reviewers'),
    view='reviewers:multiple_documents_reviewer_add'
)
link_document_multiple_reviewer_multiple_remove = Link(
    icon=icon_document_tag_multiple_remove, text=_('Remove reviewer'),
    view='reviewers:multiple_documents_selection_tag_remove'
)
link_document_multiple_reviewer_multiple_remove = Link(
    icon=icon_document_tag_multiple_remove, text=_('Remove reviewer'),
    view='reviewers:multiple_documents_selection_reviewer_remove'
)
link_document_reviewer_list = Link(
    args='resolved_object.pk', icon=icon_document_tag_list,
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
    permissions=(permission_reviewer_view,), text=_('Reviewers'),
    view='reviewers:document_reviewer_list'
)
link_document_reviewer_multiple_remove = Link(
<<<<<<< HEAD
    args='object.id', icon=icon_document_reviewer_multiple_remove,
    permissions=(permission_reviewer_remove,), text=_('Remove reviewers'),
    view='reviewers:single_document_multiple_reviewer_remove'
)
link_document_reviewer_multiple_attach = Link(
    args='object.pk', icon=icon_document_reviewer_multiple_attach,
    permissions=(permission_reviewer_attach,), text=_('Attach reviewers'),
    view='reviewers:reviewer_attach'
)
link_reviewer_create = Link(
    icon=icon_reviewer_create, permissions=(permission_reviewer_create,),
    text=_('Create new reviewer'), view='reviewers:reviewer_create'
)
link_reviewer_delete = Link(
    args='object.id', icon=icon_reviewer_delete,
    permissions=(permission_reviewer_delete,), reviewers='dangerous',
    text=_('Delete'), view='reviewers:reviewer_delete'
)
link_reviewer_edit = Link(
    args='object.id', icon=icon_reviewer_edit,
=======
    args='object.id', icon=icon_document_tag_multiple_remove,
    permissions=(permission_reviewer_remove,), text=_('Remove reviewer'),
    view='reviewers:single_document_multiple_reviewer_remove'
)
link_document_reviewer_multiple_attach = Link(
    args='object.pk', icon=icon_document_tag_multiple_attach,
    permissions=(permission_reviewer_attach,), text=_('Attach reviewers'),
    view='reviewers:reviewer_attach'
)

link_reviewer_create = Link(
    icon=icon_tag_create, permissions=(permission_reviewer_create,),
    text=_('Create new reviewer'), view='reviewers:reviewer_create'
)
link_reviewer_delete = Link(
    args='object.id', icon=icon_tag_delete,
    permissions=(permission_reviewer_delete,), tags='dangerous',
    text=_('Delete'), view='reviewers:reviewer_delete'
)
link_reviewer_edit = Link(
    args='object.id', icon=icon_tag_edit,
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
    permissions=(permission_reviewer_edit,), text=_('Edit'),
    view='reviewers:reviewer_edit'
)
link_reviewer_list = Link(
    condition=get_cascade_condition(
        app_label='reviewers', model_name='Reviewer',
        object_permission=permission_reviewer_view,
<<<<<<< HEAD
    ), icon=icon_reviewer_list,
    text=_('All'), view='reviewers:reviewer_list'
)
link_reviewer_multiple_delete = Link(
    icon=icon_reviewer_delete, permissions=(permission_reviewer_delete,),
    text=_('Delete'), view='reviewers:reviewer_multiple_delete'
)
link_reviewer_document_list = Link(
    args='object.id', icon=icon_reviewer_document_list,
=======
    ), icon=icon_tag_list,
    text=_('All'), view='reviewers:reviewer_list'
)
link_reviewer_multiple_delete = Link(
    icon=icon_tag_delete, permissions=(permission_reviewer_delete,),
    text=_('Delete'), view='reviewers:reviewer_multiple_delete'
)
link_reviewer_document_list = Link(
    args='object.id', icon=icon_tag_document_list,
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
    text=('Documents'), view='reviewers:reviewer_document_list'
)
