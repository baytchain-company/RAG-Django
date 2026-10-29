from rest_framework import serializers

from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    chunk_count = serializers.IntegerField(source="chunks.count", read_only=True)

    class Meta:
        model = Document
        fields = ["id", "title", "source", "chunk_count", "created_at"]


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    text = serializers.CharField(required=False, allow_blank=False)
    title = serializers.CharField(required=False, max_length=255)

    def validate(self, data):
        if not data.get("file") and not data.get("text"):
            raise serializers.ValidationError("Send a 'file' or a 'text'.")
        return data


class AskSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=20)
