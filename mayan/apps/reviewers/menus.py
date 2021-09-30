from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu
from mayan.apps.navigation.utils import get_cascade_condition

<<<<<<< HEAD
from .icons import icon_menu_reviewers
=======
from .icons import icon_menu_tags
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
from .permissions import permission_reviewer_create, permission_reviewer_view

menu_reviewers = Menu(
    condition=get_cascade_condition(
        app_label='reviewers', model_name='Reviewer',
        object_permission=permission_reviewer_view,
        view_permission=permission_reviewer_create,
<<<<<<< HEAD
    ), icon=icon_menu_reviewers, label=_('Reviewers'), name='reviewers'
)
=======
    ), icon=icon_menu_tags, label=_('Reviewers'), name='reviewerss'
)
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
