from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.rest_api.relations import FilteredPrimaryKeyRelatedField

from .models import Reviewer
from .permissions import permission_reviewer_attach, permission_reviewer_remove


class ReviewerSerializer(serializers.HyperlinkedModelSerializer):
    documents_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='reviewer_id',
        view_name='rest_api:reviewer-document-list'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'reviewer_id',
                'view_name': 'rest_api:reviewer-detail'
            },
        }
        fields = (
            'color', 'documents_url', 'id', 'label', 'url'
        )
        model = Reviewer


class DocumentTagAttachSerializer(serializers.Serializer):
    tag = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the tag to add to the document.'
        ), source_model=Reviewer, source_permission=permission_reviewer_attach
    )


class DocumentTagRemoveSerializer(serializers.Serializer):
    tag = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the tag to remove from the document.'
        ), source_model=Reviewer, source_permission=permission_reviewer_remove
    )
