from Rag_graph.nodes.grade_node import grade_node


def make_state_with_docs(query, docs, retrieved):
    return {
        "query": query,
        "docs": docs,
        "retrieved_docs": retrieved,
    }


def test_grade_node_relevant_without_rewrite():
    # Query matches filename
    docs = {"ProjectA/readme.md": "content here"}
    state = make_state_with_docs("readme", docs, ["ProjectA/readme.md"])
    out = grade_node(state)
    assert out["is_relevant"] is True
    assert out["relevant_count"] >= 1


def test_grade_node_rewrite_limit(monkeypatch):
    # No retrieved documents match; rewrite_count should not exceed MAX_REWRITE
    docs = {"ProjectA/readme.md": "something"}
    state = make_state_with_docs("nonmatchingquery", docs, [])

    # Ensure MAX_REWRITE is small for the test
    from Rag_graph.configs.settings import settings as _s
    monkeypatch.setattr(_s, "MAX_REWRITE", 2)

    out = grade_node(state)
    assert out.get("rewrite_count", 0) <= 2
    # is_relevant may be False; ensure the loop ended
    assert isinstance(out.get("is_relevant"), bool)
