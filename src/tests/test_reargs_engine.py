# tests/test_reargs_engine.py
import pytest
from reargs_engine.reargs_engine import ReargsEngine


@pytest.fixture
def simple_engine():
    engine = ReargsEngine(model_name="all-MiniLM-L6-v2")
    return engine


def test_build_docmap_empty_text(simple_engine):
    simple_engine.build_docmap("")
    assert len(simple_engine.docmap) == 0


def test_build_docmap_basic_paragraphs_and_sentences(simple_engine):
    text = """First paragraph with two sentences. Second one.

Second paragraph here. And another sentence!"""

    simple_engine.build_docmap(text)
    assert len(simple_engine.docmap) == 4

    keys = list(simple_engine.docmap.keys())
    assert simple_engine.docmap[keys[0]]["text"].startswith("First paragraph")
    assert simple_engine.docmap[keys[1]]["text"].startswith("Second one")
    assert "full_paragraph_text" in simple_engine.docmap[keys[0]]["metadata"]


def test_generate_similarities_requires_docmap(simple_engine):
    with pytest.raises(ValueError, match="document map is empty"):
        simple_engine.generate_similarities()


def test_generate_similarities_and_clusters_simple_case():
    engine = ReargsEngine()

    text = """The cat is on the mat.
The mat has a cat on it.
Birds fly in the sky.
Sky is very blue today."""

    engine.build_docmap(text)
    engine.generate_similarities(threshold=0.55)   # relatively low threshold

    assert len(engine.simap) > 0

    engine.generate_clusters()

    clusters = engine.get_clusters()

    # We expect at least one cluster with the cat/mat sentences
    found_cat_cluster = False
    for cluster in clusters:
        texts = [item["text"] for item in cluster]
        if "cat" in " ".join(texts).lower() and "mat" in " ".join(texts).lower():
            found_cat_cluster = True
            assert len(cluster) >= 2

    assert found_cat_cluster, "Did not find cluster containing cat and mat sentences"


def test_generate_clusters_only_groups_related_sentences():
    engine = ReargsEngine()

    text = """Apple is a fruit.
Python is a language.
Apple makes phones.
Java is also a language."""

    engine.build_docmap(text)
    engine.generate_similarities(threshold=0.4)

    engine.generate_clusters()
    clusters = engine.get_clusters()

    # Should have two main clusters: Apple-related and programming-language-related
    apple_count = 0
    lang_count = 0

    for cl in clusters:
        txt = " ".join(s["text"] for s in cl).lower()
        if "apple" in txt:
            apple_count += len(cl)
        if "language" in txt or "python" in txt or "java" in txt:
            lang_count += len(cl)

    assert apple_count >= 2
    assert lang_count >= 2


def test_clusters_have_at_least_two_sentences():
    engine = ReargsEngine()
    engine.build_docmap("One. Two. Three. Four.")
    engine.generate_similarities(threshold=0.3)   # low threshold → many connections
    engine.generate_clusters()

    for cluster in engine.get_clusters():
        assert len(cluster) >= 2, "Found singleton cluster"
