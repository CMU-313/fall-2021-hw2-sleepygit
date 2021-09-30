from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import ReviewerTestMixin


class ReviewerDocumentTestCase(DocumentTestMixin, ReviewerTestMixin, BaseTestCase):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_addition(self):
        self._create_test_reviewer()

        self.test_reviewer.attach_to(document=self.test_document)

        self.assertTrue(self.test_document in self.test_reviewer.documents.all())

    def test_document_remove(self):
        self._create_test_reviewer(add_test_document=True)

        self.test_reviewer.remove_from(document=self.test_document)

        self.assertTrue(
            self.test_document not in self.test_reviewer.documents.all()
        )


class ReviewerModuleTestCase(ReviewerTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_reviewer()

        self.assertTrue(self.test_reviewer.get_absolute_url())
