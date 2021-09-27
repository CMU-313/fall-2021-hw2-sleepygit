from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Reviewers'), name='reviewers')

permission_reviewer_create = namespace.add_permission(
    label=_('Create new reviewers'), name='reviewer_create'
)
permission_reviewer_attach = namespace.add_permission(
    label=_('Attach reviewers to documents'), name='reviewers_attach'
)
permission_reviewer_remove = namespace.add_permission(
    label=_('Remove reviewers from documents'), name='reviewers_remove'
)
permission_reviewer_delete = namespace.add_permission(
    label=_('Delete reviewers'), name='reviewer_delete'
)
permission_reviewer_view = namespace.add_permission(
    label=_('View reviewers'), name='reviewer_view'
)
permission_reviewer_edit = namespace.add_permission(
    label=_('Edit reviewers'), name='reviewer_edit'
)

