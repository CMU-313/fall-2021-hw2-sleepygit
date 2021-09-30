from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import ReviewerTestMixin


class ReviewerCopyTestCase(
    DocumentTestMixin, ReviewerTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_reviewer(add_test_document=True)
        self.test_object = self.test_reviewer
