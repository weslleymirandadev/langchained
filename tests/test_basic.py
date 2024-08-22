import os

from langchained.index import build_index, load_index, chunk_file
from langchained.search import search

SAMPLES = os.path.join(os.path.dirname(__file__), "..", "samples")


def test_find_and_chunk_files():
    from langchained.index import find_files

    files = find_files(SAMPLES)
    assert len(files) == 4
    chunks = chunk_file(files[0])
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk["source"].endswith(".md")
        assert chunk["text"]


def test_build_and_load_index(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    chunks = build_index(SAMPLES)
    assert len(chunks) > 0
    loaded = load_index()
    assert loaded == chunks


def test_search_finds_database_file():
    chunks = []
    from langchained.index import find_files

    for file in find_files(SAMPLES):
        chunks.extend(chunk_file(file))

    results = search(chunks, "how do I rotate the database credentials?")
    assert len(results) == 3
    assert results[0]["source"] == "database-rotation-runbook.md"


def test_search_respects_k():
    from langchained.index import find_files

    chunks = []
    for file in find_files(SAMPLES):
        chunks.extend(chunk_file(file))

    assert len(search(chunks, "on-call escalation", k=2)) <= 2


def test_search_no_match():
    chunks = [{"source": "a.md", "text": "hello world"}]
    assert search(chunks, "zzzz") == []


def test_ask_offline(capsys, tmp_path, monkeypatch):
    from langchained.__main__ import ask

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    build_index(SAMPLES)
    ask("how do I rotate the database credentials?")

    out = capsys.readouterr().out
    assert "offline mode" in out
    assert "rotation" in out.lower()
    assert "Sources:" in out
    assert "database-rotation-runbook.md" in out


def test_ingest_cli(tmp_path, monkeypatch, capsys):
    from langchained.__main__ import main
    import sys

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["langchained", "ingest", SAMPLES])
    main()

    out = capsys.readouterr().out
    assert "Indexed" in out
    assert os.path.exists(".langchained/index.json")
