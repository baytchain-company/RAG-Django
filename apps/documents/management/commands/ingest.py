from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.documents.loaders import UnsupportedFileType
from apps.documents.services import ingest_file

SUPPORTED = {".pdf", ".txt", ".md", ".markdown", ".rst"}


class Command(BaseCommand):
    help = "Ingest a file or every supported file in a folder: python manage.py ingest data/sample"

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, *args, path, **options):
        target = Path(path)
        if not target.exists():
            raise CommandError(f"Not found: {target}")
        files = [target] if target.is_file() else sorted(p for p in target.rglob("*") if p.suffix.lower() in SUPPORTED)
        for file in files:
            try:
                doc = ingest_file(file)
            except UnsupportedFileType as exc:
                self.stderr.write(str(exc))
                continue
            self.stdout.write(self.style.SUCCESS(f"✓ {file.name}: {doc.chunks.count()} chunks"))
