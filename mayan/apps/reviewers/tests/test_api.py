from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_reviewer_attached, event_reviewer_created, event_reviewer_edited, event_reviewer_removed
)
from ..models import Reviewer
from ..permissions import (
    permission_reviewer_attach, permission_reviewer_create, permission_reviewer_delete,
    permission_reviewer_edit, permission_reviewer_remove, permission_reviewer_view
)

from .mixins import ReviewerAPIViewTestMixin, ReviewerTestMixin


class ReviewerAPIViewTestCase(ReviewerAPIViewTestMixin, ReviewerTestMixin, BaseAPITestCase):
    def test_reviewer_create_api_view_no_permission(self):
        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Reviewer.objects.count(), reviewer_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_reviewer_create)

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Reviewer.objects.count(), reviewer_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_reviewer)
        self.assertEqual(events[0].verb, event_reviewer_created.id)

    def test_reviewer_delete_api_view_no_permission(self):
        self._create_test_reviewer()

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Reviewer.objects.count(), reviewer_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_delete_api_view_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_delete)

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Reviewer.objects.count(), reviewer_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_detail_api_view_no_permission(self):
        self._create_test_reviewer()

        self._clear_events()

        response = self._request_test_reviewer_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_detail_api_view_with_access(self):
        self._create_test_reviewer()
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_view
        )

        self._clear_events()

        response = self._request_test_reviewer_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], self.test_reviewer.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_edit_api_view_via_patch_no_permission(self):
        self._create_test_reviewer()

        reviewer_label = self.test_reviewer.label
        reviewer_color = self.test_reviewer.color

        self._clear_events()

        response = self._request_test_reviewer_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_reviewer.refresh_from_db()
        self.assertEqual(self.test_reviewer.label, reviewer_label)
        self.assertEqual(self.test_reviewer.color, reviewer_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_edit_api_view_via_patch_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_edit)

        reviewer_label = self.test_reviewer.label
        reviewer_color = self.test_reviewer.color

        self._clear_events()

        response = self._request_test_reviewer_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_reviewer.refresh_from_db()
        self.assertNotEqual(self.test_reviewer.label, reviewer_label)
        self.assertNotEqual(self.test_reviewer.color, reviewer_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_reviewer)
        self.assertEqual(events[0].verb, event_reviewer_edited.id)

    def test_reviewer_edit_api_view_via_put_no_permission(self):
        self._create_test_reviewer()

        reviewer_label = self.test_reviewer.label
        reviewer_color = self.test_reviewer.color

        self._clear_events()

        response = self._request_test_reviewer_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_reviewer.refresh_from_db()
        self.assertEqual(self.test_reviewer.label, reviewer_label)
        self.assertEqual(self.test_reviewer.color, reviewer_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_edit_api_view_via_put_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_edit)

        reviewer_label = self.test_reviewer.label
        reviewer_color = self.test_reviewer.color

        self._clear_events()

        response = self._request_test_reviewer_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_reviewer.refresh_from_db()
        self.assertNotEqual(self.test_reviewer.label, reviewer_label)
        self.assertNotEqual(self.test_reviewer.color, reviewer_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_reviewer)
        self.assertEqual(events[0].verb, event_reviewer_edited.id)

    def test_reviewer_list_api_view_no_permission(self):
        self._create_test_reviewer()

        self._clear_events()

        response = self._request_test_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_list_api_view_with_access(self):
        self._create_test_reviewer()
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_view
        )

        self._clear_events()

        response = self._request_test_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_reviewer.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class ReviewerDocumentAPIViewTestCase(
    DocumentTestMixin, ReviewerAPIViewTestMixin, ReviewerTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_reviewer()
        self._create_test_document_stub()

    def test_reviewer_document_list_api_view_no_permission(self):
        self.test_reviewer.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_reviewer_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_api_view_with_reviewer_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_reviewer_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_api_view_with_document_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self._clear_events()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_reviewer_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_api_view_with_full_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_reviewer_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(s=self.test_document.uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_trashed_document_list_api_view_with_full_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_reviewer_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentReviewerAPIViewTestCase(
    DocumentTestMixin, ReviewerAPIViewTestMixin, ReviewerTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_reviewer()
        self._create_test_document_stub()

    def test_document_attach_reviewer_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_reviewer_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_reviewer_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )

        self._clear_events()

        response = self._request_test_document_reviewer_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_reviewer_api_view_with_reviewer_access(self):
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_attach
        )

        self._clear_events()

        response = self._request_test_document_reviewer_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_reviewer_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_attach
        )

        self._clear_events()

        response = self._request_test_document_reviewer_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_reviewer)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_reviewer_attached.id)

    def test_trashed_document_attach_reviewer_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_attach
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_reviewer_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_list_api_view_no_permission(self):
        self.test_reviewer.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_document_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_list_api_view_with_document_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )

        self._clear_events()

        response = self._request_test_document_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_list_api_view_with_reviewer_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_document_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_list_api_view_with_full_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_document_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.test_reviewer.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_reviewer_list_api_view_with_full_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_reviewer_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_remove_api_view_no_permission(self):
        self.test_reviewer.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_document_reviewer_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_remove_api_view_with_document_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )

        self._clear_events()

        response = self._request_test_document_reviewer_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_remove_api_view_with_reviewer_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self._clear_events()

        response = self._request_test_document_reviewer_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_remove_api_view_with_full_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self._clear_events()

        response = self._request_test_document_reviewer_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_reviewer)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_reviewer_removed.id)

    def test_trashed_document_reviewer_remove_api_view_with_full_access(self):
        self.test_reviewer.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_reviewer_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
