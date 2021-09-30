from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.document_indexing.models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .literals import (
    TEST_TAG_INDEX_HAS_TAG, TEST_TAG_INDEX_NO_TAG,
    TEST_TAG_INDEX_NODE_TEMPLATE
)
from .mixins import ReviewerTestMixin


class ReviewerSignalIndexingTestCase(
    DocumentTestMixin, IndexTemplateTestMixin, ReviewerTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def test_reviewer_indexing(self):
        self._create_test_reviewer()
        self._create_test_index_template(add_test_document_type=True)

        root = self.test_index_template.template_root
        self.test_index_template.node_templates.create(
            parent=root, expression=TEST_TAG_INDEX_NODE_TEMPLATE,
            link_documents=True
        )

        self._create_test_document_stub()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )

        self.test_reviewer.documents.add(self.test_document)

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_HAS_TAG
            ).documents.all()
        )

        self.test_reviewer.delete()

        self.assertTrue(
            self.test_document in IndexInstanceNode.objects.get(
                value=TEST_TAG_INDEX_NO_TAG
            ).documents.all()
        )
