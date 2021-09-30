from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from django.db.models import Q

from ..models import Reviewer

from .literals import (
    TEST_TAG_COLOR, TEST_TAG_COLOR_EDITED, TEST_TAG_LABEL,
    TEST_TAG_LABEL_EDITED
)


class DocumentReviewerViewTestMixin:
    def _request_test_document_reviewer_attach_view(self):
        return self.post(
            viewname='reviewers:reviewer_attach', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'reviewers': self.test_reviewer.pk,
                'user': self._test_case_user.pk
            }
        )

    def _request_test_document_multiple_reviewer_multiple_attach_view(self):
        return self.post(
            viewname='reviewers:multiple_documents_reviewer_attach', data={
                'id_list': self.test_document.pk, 'reviewers': self.test_reviewer.pk,
                'user': self._test_case_user.pk
            }
        )

    def _request_test_document_reviewer_multiple_remove_view(self):
        return self.post(
            viewname='reviewers:single_document_multiple_reviewer_remove', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'reviewers': self.test_reviewer.pk,
            }
        )

    def _request_test_document_multiple_reviewer_remove_view(self):
        return self.post(
            viewname='reviewers:multiple_documents_selection_reviewer_remove', data={
                'id_list': self.test_document.pk,
                'reviewers': self.test_reviewer.pk,
            }
        )

    def _request_test_document_reviewer_list_view(self):
        return self.get(
            viewname='reviewers:document_reviewer_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_reviewer_document_list_view(self):
        return self.get(
            viewname='reviewers:reviewer_document_list', kwargs={
                'reviewer_id': self.test_reviewer.pk
            }
        )


class ReviewerAPIViewTestMixin:
    def _request_test_document_reviewer_attach_api_view(self):
        return self.post(
            viewname='rest_api:document-reviewer-attach', kwargs={
                'document_id': self.test_document.pk
            }, data={'reviewer': self.test_reviewer.pk}
        )

    def _request_test_document_reviewer_list_api_view(self):
        return self.get(
            viewname='rest_api:document-reviewer-list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_reviewer_remove_api_view(self):
        return self.post(
            viewname='rest_api:document-reviewer-remove', kwargs={
                'document_id': self.test_document.pk
            }, data={'reviewer': self.test_reviewer.pk}
        )

    def _request_test_reviewer_create_api_view(self):
        pk_list = list(Reviewer.objects.values('pk'))

        response = self.post(
            viewname='rest_api:reviewer-list', data={
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

        try:
            self.test_reviewer = Reviewer.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Reviewer.DoesNotExist:
            self.test_reviewer = None

        return response

    def _request_test_reviewer_delete_api_view(self):
        return self.delete(
            viewname='rest_api:reviewer-detail',
            kwargs={'reviewer_id': self.test_reviewer.pk}
        )

    def _request_test_reviewer_detail_api_view(self):
        return self.get(
            viewname='rest_api:reviewer-detail',
            kwargs={'reviewer_id': self.test_reviewer.pk}
        )

    def _request_test_reviewer_document_list_api_view(self):
        return self.get(
            viewname='rest_api:reviewer-document-list', kwargs={
                'reviewer_id': self.test_reviewer.pk
            }
        )

    def _request_test_reviewer_edit_api_view(self, extra_data=None, verb='patch'):
        data = {
            'label': TEST_TAG_LABEL_EDITED,
            'color': TEST_TAG_COLOR_EDITED
        }

        if extra_data:
            data.update(extra_data)

        return getattr(self, verb)(
            viewname='rest_api:reviewer-detail',
            kwargs={'reviewer_id': self.test_reviewer.pk},
            data=data
        )

    def _request_test_reviewer_list_api_view(self):
        return self.get(viewname='rest_api:reviewer-list')


class ReviewerTestMixin:
    def setUp(self):
        super().setUp()
        self.test_reviewers = []

    def _create_test_reviewer(self, add_test_document=False):
        total_test_labels = len(self.test_reviewers)
        label = '{}_{}'.format(TEST_TAG_LABEL, total_test_labels)

        self.test_reviewer = Reviewer.objects.create(
            color=TEST_TAG_COLOR, label=label
        )

        self.test_reviewers.append(self.test_reviewer)

        if add_test_document:
            self.test_reviewer.documents.add(self.test_document)


class ReviewerViewTestMixin:
    def _request_test_reviewer_create_view(self):
        pk_list = list(Reviewer.objects.values('pk'))

        response = self.post(
            viewname='reviewers:reviewer_create', data={
                'label': TEST_TAG_LABEL,
                'color': TEST_TAG_COLOR
            }
        )

        try:
            self.test_reviewer = Reviewer.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Reviewer.DoesNotExist:
            self.test_reviewer = None

        return response

    def _request_test_reviewer_delete_view(self):
        return self.post(
            viewname='reviewers:reviewer_delete', kwargs={'reviewer_id': self.test_reviewer.pk}
        )

    def _request_test_reviewer_delete_multiple_view(self):
        return self.post(
            viewname='reviewers:reviewer_multiple_delete', data={
                'id_list': self.test_reviewer.pk
            },
        )

    def _request_test_reviewer_edit_view(self):
        return self.post(
            viewname='reviewers:reviewer_edit', kwargs={
                'reviewer_id': self.test_reviewer.pk
            }, data={
                'label': TEST_TAG_LABEL_EDITED, 'color': TEST_TAG_COLOR_EDITED
            }
        )

    def _request_test_reviewer_list_view(self):
        return self.get(viewname='reviewers:reviewer_list')


class ReviewergedDocumentUploadWizardStepViewTestMixin:
    def _request_upload_interactive_document_create_view(self):
        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'document_type_id': self.test_document_type.pk,
                    'source-file': file_object,
                    'reviewers': Reviewer.objects.values_list('pk', flat=True)
                }
            )
