import pytest
from app.agents.search import SearchClient

def test_url_normalization():
    client = SearchClient()
    url1 = "https://example.com/path/?utm_source=twitter"
    url2 = "https://example.com/path/"
    assert client.normalize_url(url1) == "https://example.com/path"
    assert client.normalize_url(url2) == "https://example.com/path"

def test_publisher_extraction():
    client = SearchClient()
    assert "arxiv" in client.extract_publisher("https://arxiv.org/abs/2401.0001").lower()
    assert "berkeley" in client.extract_publisher("https://bair.berkeley.edu/blog/").lower() or "bair" in client.extract_publisher("https://bair.berkeley.edu/blog/").lower()

def test_curated_fallback_sources():
    client = SearchClient()
    sources = client._get_curated_fallback_sources("GenAI skills 2027")
    assert len(sources) >= 3
    assert any("compound" in s.title.lower() for s in sources)
