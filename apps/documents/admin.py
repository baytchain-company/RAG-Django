from django.contrib import admin

from .models import Chunk, Document


class ChunkInline(admin.TabularInline):
    model = Chunk
    fields = ("index", "page", "text")
    readonly_fields = fields
    extra = 0
    can_delete = False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "chunk_count", "created_at")
    inlines = [ChunkInline]

    @admin.display(description="Chunks")
    def chunk_count(self, obj):
        return obj.chunks.count()
