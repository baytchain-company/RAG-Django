from django.urls import path

from .views import AskView, DocumentDeleteView, DocumentListCreateView

urlpatterns = [
    path("documents/", DocumentListCreateView.as_view(), name="documents"),
    path("documents/<int:pk>/", DocumentDeleteView.as_view(), name="document-delete"),
    path("ask/", AskView.as_view(), name="ask"),
]
