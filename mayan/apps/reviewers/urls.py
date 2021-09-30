from django.conf.urls import url

from .api_views import (
    APIDocumentReviewerAttachView, APIDocumentReviewerRemoveView,
    APIDocumentReviewerListView, APIReviewerDocumentListView, APIReviewerListView,
    APIReviewerDetailView
)
from .views import (
    DocumentReviewerListView, ReviewerAttachActionView, ReviewerCreateView,
    ReviewerDeleteActionView, ReviewerEditView, ReviewerListView, ReviewerRemoveActionView,
    ReviewerDocumentListView,
    DocumentReviewerListView, ReviewerAddActionView, ReviewerCreateView,
    ReviewerDeleteActionView, ReviewerEditView, ReviewerListView, ReviewerRemoveActionView,
    ReviewerDocumentListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/reviewers/$',
        name='document_reviewer_list', view=DocumentReviewerListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/reviewers/multiple/attach/$',
        name='reviewer_attach', view=ReviewerAttachActionView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/reviewers/multiple/add/$',
        name='reviewer_add', view=ReviewerAttachActionView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/reviewers/multiple/remove/$',
        name='single_document_multiple_reviewer_remove',
        view=ReviewerRemoveActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/reviewers/multiple/remove/$',
        name='multiple_documents_selection_reviewer_remove',
        view=ReviewerRemoveActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/reviewers/multiple/attach/$',
        name='multiple_documents_reviewer_attach',
        view=ReviewerAttachActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/reviewers/multiple/add/$',
        name='multiple_documents_reviewer_add',
        view=ReviewerAddActionView.as_view()
    ),
    url(regex=r'^reviewers/$', name='reviewer_list', view=ReviewerListView.as_view()),
    url(
        regex=r'^reviewers/create/$', name='reviewer_create',
        view=ReviewerCreateView.as_view()
    ),
    url(
        regex=r'^reviewers/(?P<reviewer_id>\d+)/delete/$', name='reviewer_delete',
        view=ReviewerDeleteActionView.as_view()
    ),
    url(
        regex=r'^reviewers/(?P<reviewer_id>\d+)/edit/$', name='reviewer_edit',
        view=ReviewerEditView.as_view()
    ),
    url(
        regex=r'^reviewers/(?P<reviewer_id>\d+)/documents/$', name='reviewer_document_list',
        view=ReviewerDocumentListView.as_view()
    ),
    url(
        regex=r'^reviewers/multiple/delete/$', name='reviewer_multiple_delete',
        view=ReviewerDeleteActionView.as_view()
    ),
]

api_urls = [
    url(regex=r'^reviewers/$', view=APIReviewerListView.as_view(), name='reviewer-list'),
    url(
        regex=r'^reviewers/(?P<reviewer_id>[0-9]+)/$', view=APIReviewerDetailView.as_view(),
        name='reviewer-detail'
    ),
    url(
        regex=r'^reviewers/(?P<reviewer_id>[0-9]+)/documents/$',
        view=APIReviewerDocumentListView.as_view(), name='reviewer-document-list'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/reviewers/$',
        view=APIDocumentReviewerListView.as_view(), name='document-reviewer-list'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/reviewers/attach/$',
        name='document-reviewer-attach', view=APIDocumentReviewerAttachView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/reviewers/remove/$',
        name='document-reviewer-remove', view=APIDocumentReviewerRemoveView.as_view()
    ),
]
