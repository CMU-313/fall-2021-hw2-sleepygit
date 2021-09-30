from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers.document_serializers import (
    DocumentSerializer
)
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .models import Reviewer
from .permissions import (
    permission_reviewer_attach, permission_reviewer_create, permission_reviewer_delete,
    permission_reviewer_edit, permission_reviewer_remove, permission_reviewer_view
)
from .serializers import (
    DocumentReviewerAttachSerializer, DocumentReviewerRemoveSerializer,
    ReviewerSerializer
)


class APIReviewerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected reviewer.
    get: Return the details of the selected reviewer.
    patch: Edit the selected reviewer.
    put: Edit the selected reviewer.
    """
    lookup_url_kwarg = 'reviewer_id'
    mayan_object_permissions = {
        'DELETE': (permission_reviewer_delete,),
        'GET': (permission_reviewer_view,),
        'PATCH': (permission_reviewer_edit,),
        'PUT': (permission_reviewer_edit,)
    }
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIReviewerListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the reviewers.
    post: Create a new reviewer.
    """
    mayan_object_permissions = {'GET': (permission_reviewer_view,)}
    mayan_view_permissions = {'POST': (permission_reviewer_create,)}
    ordering_fields = ('label',)
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIReviewerDocumentListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
<<<<<<< HEAD
    get: Returns a list of all the documents reviewerged by a particular reviewer.
=======
    get: Returns a list of all the documents tagged by a particular reviewer.
>>>>>>> 8a29a6a6d9e0878c07ded56efd2ea18caddea7a7
    """
    external_object_class = Reviewer
    external_object_pk_url_kwarg = 'reviewer_id'
    mayan_external_object_permissions = {'GET': (permission_reviewer_view,)}
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.valid.filter(
            pk__in=self.external_object.documents.only('pk')
        )


class APIDocumentReviewerAttachView(generics.ObjectActionAPIView):
    """
    post: Attach a reviewer to a document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_reviewer_attach,)
    }
    serializer_class = DocumentReviewerAttachSerializer
    queryset = Document.valid

    def object_action(self, request, serializer):
        reviewer = serializer.validated_data['reviewer']
        reviewer._event_actor = self.request.user
        reviewer.attach_to(document=self.object)


class APIDocumentReviewerRemoveView(generics.ObjectActionAPIView):
    """
    post: Remove a reviewer from a document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_reviewer_remove,)
    }
    serializer_class = DocumentReviewerRemoveSerializer
    queryset = Document.valid

    def object_action(self, request, serializer):
        reviewer = serializer.validated_data['reviewer']
        reviewer._event_actor = self.request.user
        reviewer.remove_from(document=self.object)


class APIDocumentReviewerListView(ExternalObjectAPIViewMixin, generics.ListAPIView):
    """
    get: Returns a list of all the reviewers attached to a document.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permissions = {
        'GET': (permission_reviewer_view,)
    }
    mayan_object_permissions = {
        'GET': (permission_reviewer_view,),
    }
    serializer_class = ReviewerSerializer

    def get_queryset(self):
        return self.external_object.reviewers.all()
