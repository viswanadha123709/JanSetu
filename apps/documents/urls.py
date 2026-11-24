from django.urls import path
from apps.documents.views import (
    DocumentUploadView,
    DocumentSampleLoadView,
    DocumentDetailView,
    DocumentClausesView,
    DocumentQAView,
    DocumentListView,
)

urlpatterns = [
    path('documents/upload/', DocumentUploadView.as_view(), name='doc_upload'),
    path('documents/sample/', DocumentSampleLoadView.as_view(), name='doc_sample_load'),
    path('documents/', DocumentListView.as_view(), name='doc_list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='doc_detail'),
    path('documents/<int:pk>/clauses/', DocumentClausesView.as_view(), name='doc_clauses'),
    path('documents/<int:pk>/ask/', DocumentQAView.as_view(), name='doc_qa'),
]
