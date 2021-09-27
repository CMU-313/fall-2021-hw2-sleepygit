from django.conf.urls import url

from .api_views import (
    APIDocumentTagAttachView, APIDocumentTagRemoveView,
    APIDocumentTagListView, APITagDocumentListView, APITagListView,
    APITagDetailView
)
from .views import (
    DocumentReviewerListView, ReviewerAddActionView, ReviewerCreateView,
    ReviewerDeleteActionView, ReviewerEditView, ReviewerListView, ReviewerRemoveActionView,
    ReviewerDocumentListView, ReviewerActionView, ReviewerAttachActionView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/reviewers/$',
        name='document_reviewer_list', view=DocumentReviewerListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/tags/multiple/attach/$',
        name='tag_attach', view=ReviewerActionView.as_view()
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
        regex=r'^documents/multiple/tags/multiple/attach/$',
        name='multiple_documents_tag_attach',
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
        regex=r'^reviewers/(?P<tag_id>\d+)/delete/$', name='reviewer_delete',
        view=ReviewerDeleteActionView.as_view()
    ),
    url(
        regex=r'^reviewers/(?P<tag_id>\d+)/edit/$', name='reviewer_edit',
        view=ReviewerEditView.as_view()
    ),
    url(
        regex=r'^reviewers/(?P<tag_id>\d+)/documents/$', name='reviewer_document_list',
        view=ReviewerDocumentListView.as_view()
    ),
    url(
        regex=r'^reviewers/multiple/delete/$', name='reviewer_multiple_delete',
        view=ReviewerDeleteActionView.as_view()
    )
]

api_urls = [
    url(regex=r'^tags/$', view=APITagListView.as_view(), name='tag-list'),
    url(
        regex=r'^tags/(?P<tag_id>[0-9]+)/$', view=APITagDetailView.as_view(),
        name='tag-detail'
    ),
    url(
        regex=r'^tags/(?P<tag_id>[0-9]+)/documents/$',
        view=APITagDocumentListView.as_view(), name='tag-document-list'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/tags/$',
        view=APIDocumentTagListView.as_view(), name='document-tag-list'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/tags/attach/$',
        name='document-tag-attach', view=APIDocumentTagAttachView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/tags/remove/$',
        name='document-tag-remove', view=APIDocumentTagRemoveView.as_view()
    ),
]
