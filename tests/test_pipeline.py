import pytest
from rest_framework.test import APIClient

from apps.documents.services import ingest_text
from apps.rag.pipeline import NOT_FOUND, ask

HANDBOOK = [
    (1, "Every employee gets 24 paid vacation days per year. Request vacation two weeks in advance."),
    (2, "Salaries are paid on the 5th of every month."),
    (3, "New employees receive a MacBook Pro and a monitor on day one."),
]


@pytest.mark.django_db
def test_ingest_creates_chunks():
    doc = ingest_text("Handbook", HANDBOOK)
    assert doc.chunks.count() == 3


@pytest.mark.django_db
def test_ask_returns_the_right_source():
    ingest_text("Handbook", HANDBOOK)
    result = ask("How many vacation days do employees get?", top_k=1)
    assert result["sources"][0]["page"] == 1
    assert "24" in result["answer"]


@pytest.mark.django_db
def test_ask_without_documents_says_not_found():
    assert ask("Anything?")["answer"] == NOT_FOUND


@pytest.mark.django_db
def test_api_upload_and_ask():
    client = APIClient()
    r = client.post("/api/documents/", {"title": "Pay", "text": "Salaries are paid on the 5th of every month."}, format="json")
    assert r.status_code == 201 and r.json()["chunk_count"] == 1
    r = client.post("/api/ask/", {"question": "When are salaries paid?"}, format="json")
    assert r.status_code == 200
    assert r.json()["sources"][0]["document"] == "Pay"
