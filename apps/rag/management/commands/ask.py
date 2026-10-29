from django.core.management.base import BaseCommand

from apps.rag.pipeline import ask


class Command(BaseCommand):
    help = 'Ask a question from the terminal: python manage.py ask "How many vacation days do I get?"'

    def add_arguments(self, parser):
        parser.add_argument("question")
        parser.add_argument("--top-k", type=int, default=None)

    def handle(self, *args, question, top_k, **options):
        result = ask(question, top_k=top_k)
        self.stdout.write(self.style.SUCCESS("\nANSWER\n") + result["answer"] + "\n")
        for s in result["sources"]:
            where = s["document"] + (f" p.{s['page']}" if s["page"] else "")
            self.stdout.write(f"[{s['n']}] {where} · chunk {s['index']} · distance {s['distance']}")
