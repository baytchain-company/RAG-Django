import tempfile
from pathlib import Path

from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.documents.loaders import UnsupportedFileType
from apps.documents.models import Document
from apps.documents.services import ingest_file, ingest_text
from apps.rag.pipeline import ask

from .serializers import AskSerializer, DocumentSerializer, UploadSerializer


class DocumentListCreateView(generics.ListCreateAPIView):
    """GET: list documents. POST: upload a file (pdf/txt/md) or raw text."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        data = UploadSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        upload, title = data.validated_data.get("file"), data.validated_data.get("title")
        try:
            if upload:
                suffix = Path(upload.name).suffix
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
                    for part in upload.chunks():
                        tmp.write(part)
                    tmp.flush()
                    doc = ingest_file(tmp.name, title=title or Path(upload.name).stem)
                doc.source = upload.name
                doc.save(update_fields=["source"])
            else:
                doc = ingest_text(title or "Pasted text", [(None, data.validated_data["text"])])
        except UnsupportedFileType as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)


class DocumentDeleteView(generics.DestroyAPIView):
    queryset = Document.objects.all()


class AskView(APIView):
    """POST {"question": "...", "top_k": 4} -> {"answer": "...", "sources": [...]}"""

    def post(self, request):
        data = AskSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(ask(data.validated_data["question"], data.validated_data.get("top_k")))
