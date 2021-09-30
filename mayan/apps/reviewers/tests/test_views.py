from django.utils.encoding import force_text

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_reviewer_attached, event_reviewer_created, event_reviewer_edited,
    event_reviewer_removed
)
from ..links import link_reviewer_edit
from ..models import Reviewer
from ..permissions import (
    permission_reviewer_attach, permission_reviewer_create, permission_reviewer_delete,
    permission_reviewer_edit, permission_reviewer_remove, permission_reviewer_view
)

from .mixins import DocumentReviewerViewTestMixin, ReviewerTestMixin, ReviewerViewTestMixin


class DocumentReviewerViewTestCase(
    DocumentReviewerViewTestMixin, ReviewerTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_reviewers_list_no_permission(self):
        self._create_test_reviewer(add_test_document=True)

        self._clear_events()

        response = self._request_test_document_reviewer_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_reviewer), status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewers_list_with_document_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )

        self._clear_events()

        response = self._request_test_document_reviewer_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_reviewer), status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewers_list_with_reviewer_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_document_reviewer_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_reviewer), status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewers_list_with_full_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_view
        )

        self._clear_events()

        response = self._request_test_document_reviewer_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_reviewer),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_reviewers_list_with_full_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_reviewer_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewers_list_reviewer_edit_link_with_full_access(self):
        # Ensure that DocumentReviewer instances and links are
        # resolved in this view and not base Reviewer instances.
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_view
        )
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_view
        )
        self.grant_access(
            obj=self.test_reviewer, permission=permission_reviewer_edit
        )

        self._clear_events()

        response = self._request_test_document_reviewer_list_view()

        link_context = response.context[-1]
        link_context['object'] = self.test_reviewer

        result = link_reviewer_edit.resolve(context=link_context)

        self.assertNotContains(
            response=response, text=result.url,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_attach_view_no_permission(self):
        self._create_test_reviewer()

        self._clear_events()

        response = self._request_test_document_reviewer_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_attach_view_with_reviewer_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_attach)

        self._clear_events()

        response = self._request_test_document_reviewer_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_attach_view_with_document_access(self):
        self._create_test_reviewer()

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )

        self._clear_events()

        response = self._request_test_document_reviewer_attach_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_attach_view_with_full_access(self):
        self._create_test_reviewer()

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_attach)

        self._clear_events()

        response = self._request_test_document_reviewer_attach_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_reviewer)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_reviewer_attached.id)

    def test_trashed_document_reviewer_attach_view_with_full_access(self):
        self._create_test_reviewer()

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_attach)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_reviewer_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_attach_view_no_permission(self):
        self._create_test_reviewer()

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_multiple_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_attach_view_with_reviewer_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_attach)

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_multiple_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_attach_view_with_document_access(self):
        self._create_test_reviewer()

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_multiple_attach_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_attach_view_with_full_access(self):
        self._create_test_reviewer()

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_attach)

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_multiple_attach_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_reviewer)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_reviewer_attached.id)

    def test_trashed_document_multiple_reviewer_attach_view_with_full_access(self):
        self._create_test_reviewer()

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_attach
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_attach)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_multiple_attach_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_multiple_remove_view_no_permission(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self._clear_events()

        response = self._request_test_document_reviewer_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_multiple_remove_view_with_reviewer_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self._clear_events()

        response = self._request_test_document_reviewer_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_multiple_remove_view_with_document_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )

        self._clear_events()

        response = self._request_test_document_reviewer_multiple_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_reviewer_multiple_remove_view_with_full_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self._clear_events()

        response = self._request_test_document_reviewer_multiple_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_reviewer)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_reviewer_removed.id)

    def test_trashed_document_reviewer_multiple_remove_view_with_full_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_reviewer_multiple_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_multiple_remove_view_no_permission(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_remove_view_with_reviewer_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_remove_view_with_document_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_multiple_reviewer_remove_view_with_full_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_reviewer not in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_reviewer)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_reviewer_removed.id)

    def test_trashed_document_multiple_reviewer_remove_view_with_full_access(self):
        self._create_test_reviewer()
        self.test_document.reviewers.add(self.test_reviewer)

        self.grant_access(
            obj=self.test_document, permission=permission_reviewer_remove
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_remove)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_multiple_reviewer_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_reviewer in self.test_document.reviewers.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_with_no_permission(self):
        self._create_test_reviewer(add_test_document=True)

        self._clear_events()

        response = self._request_test_reviewer_document_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_with_reviewer_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_reviewer_document_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_reviewer),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_document),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_with_document_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_reviewer_document_list_view()
        self.assertNotContains(
            response=response, text=force_text(s=self.test_reviewer),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_document),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_document_list_with_full_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_reviewer_document_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_reviewer),
            status_code=200
        )
        self.assertContains(
            response=response, text=force_text(s=self.test_document),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_trashed_document_list_with_full_access(self):
        self._create_test_reviewer(add_test_document=True)

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_reviewer_document_list_view()
        self.assertContains(
            response=response, text=force_text(s=self.test_reviewer),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=force_text(s=self.test_document),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class ReviewerViewTestCase(ReviewerTestMixin, ReviewerViewTestMixin, GenericViewTestCase):
    def test_reviewer_create_view_no_permission(self):
        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Reviewer.objects.count(), reviewer_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_create_view_with_permissions(self):
        self.grant_permission(permission=permission_reviewer_create)

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Reviewer.objects.count(), reviewer_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_reviewer)
        self.assertEqual(events[0].verb, event_reviewer_created.id)

    def test_reviewer_delete_view_no_permission(self):
        self._create_test_reviewer()

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Reviewer.objects.count(), reviewer_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_delete_view_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_delete)

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Reviewer.objects.count(), reviewer_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_multiple_delete_view_no_permission(self):
        self._create_test_reviewer()

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_delete_multiple_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Reviewer.objects.count(), reviewer_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_multiple_delete_view_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_delete)

        reviewer_count = Reviewer.objects.count()

        self._clear_events()

        response = self._request_test_reviewer_delete_multiple_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Reviewer.objects.count(), reviewer_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_edit_view_no_permission(self):
        self._create_test_reviewer()

        reviewer_label = self.test_reviewer.label

        self._clear_events()

        response = self._request_test_reviewer_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_reviewer.refresh_from_db()
        self.assertEqual(self.test_reviewer.label, reviewer_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_edit_view_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_edit)

        reviewer_label = self.test_reviewer.label

        self._clear_events()

        response = self._request_test_reviewer_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_reviewer.refresh_from_db()
        self.assertNotEqual(self.test_reviewer.label, reviewer_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_reviewer)
        self.assertEqual(events[0].verb, event_reviewer_edited.id)

    def test_reviewer_list_view_with_no_permission(self):
        self._create_test_reviewer()

        self._clear_events()

        response = self._request_test_reviewer_list_view()
        self.assertNotContains(
            response=response, text=self.test_reviewer.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_reviewer_list_view_with_access(self):
        self._create_test_reviewer()

        self.grant_access(obj=self.test_reviewer, permission=permission_reviewer_view)

        self._clear_events()

        response = self._request_test_reviewer_list_view()
        self.assertContains(
            response=response, text=self.test_reviewer.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
