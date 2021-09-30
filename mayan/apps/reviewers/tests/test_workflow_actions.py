from mayan.apps.document_states.permissions import permission_workflow_template_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.document_states.tests.mixins.workflow_template_state_mixins import WorkflowTemplateStateActionViewTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..models import Reviewer
from ..workflow_actions import AttachReviewerAction, RemoveReviewerAction

from .mixins import ReviewerTestMixin


class ReviewerWorkflowActionTestCase(ReviewerTestMixin, ActionTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_reviewer()

    def test_reviewer_attach_action(self):
        action = AttachReviewerAction(form_data={'reviewers': Reviewer.objects.all()})
        action.execute(context={'document': self.test_document})

        self.assertEqual(self.test_reviewer.documents.count(), 1)
        self.assertTrue(self.test_document in self.test_reviewer.documents.all())

    def test_reviewer_remove_action(self):
        self.test_reviewer.attach_to(document=self.test_document)

        action = RemoveReviewerAction(form_data={'reviewers': Reviewer.objects.all()})
        action.execute(context={'document': self.test_document})

        self.assertEqual(self.test_reviewer.documents.count(), 0)


class ReviewerWorkflowActionViewTestCase(
    WorkflowTemplateStateActionViewTestMixin, WorkflowTemplateTestMixin, GenericViewTestCase
):
    def test_reviewer_attach_action_create_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.reviewers.workflow_actions.AttachReviewerAction'
        )
        self.assertEqual(response.status_code, 302)

    def test_reviewer_remove_action_create_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.reviewers.workflow_actions.RemoveReviewerAction'
        )
        self.assertEqual(response.status_code, 302)
