import django.db.models.deletion
import pgvector.django
from django.conf import settings
from django.db import migrations, models
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        VectorExtension(),  # CREATE EXTENSION IF NOT EXISTS vector
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("source", models.CharField(blank=True, help_text="File name or URL", max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Chunk",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("index", models.PositiveIntegerField(help_text="Position inside the document")),
                ("page", models.PositiveIntegerField(blank=True, null=True)),
                ("text", models.TextField()),
                # Dimension comes from settings.RAG["EMBEDDING_DIM"] (must match your embedding model).
                ("embedding", pgvector.django.VectorField(dimensions=settings.RAG["EMBEDDING_DIM"])),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chunks",
                        to="documents.document",
                    ),
                ),
            ],
            options={
                "ordering": ["document_id", "index"],
                "indexes": [
                    pgvector.django.HnswIndex(
                        ef_construction=64,
                        fields=["embedding"],
                        m=16,
                        name="chunk_embedding_hnsw",
                        opclasses=["vector_cosine_ops"],
                    )
                ],
            },
        ),
    ]
