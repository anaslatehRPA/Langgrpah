import pytest

from Rag_graph.nodes.document_loader_node import load_project_documents
from Rag_graph.nodes.retriever_node import retriever_node
from Rag_graph.nodes.grade_node import grade_node
from Rag_graph.configs.settings import settings


def test_rewrite_respects_max_rewrites():
    """If query cannot be matched, rewrite_count should stop at MAX_REWRITES."""
    # arrange: load documents into state from repo data folder
    state = {}
    state = load_project_documents(state, data_root="data")

    # ensure docs exist (loader uses repo data folder)
    assert "docs" in state

    # set a query that is unlikely to match any document
    state["query"] = "this-query-should-not-match-anything-xyz"

    # set MAX_REWRITES small for the test
    orig_max = getattr(settings, "MAX_REWRITES", None)
    # Pydantic Settings doesn't allow setting unknown fields via normal setattr.
    # Use object.__setattr__ to inject the attribute for testing only.
    object.__setattr__(settings, "MAX_REWRITES", 2)

    try:
        # initial retrieval
        state = retriever_node(state)
        # run grade node which may rewrite and re-retrieve
        result = grade_node(state)

        # rewrite_count should not exceed MAX_REWRITES
        assert result.get("rewrite_count", 0) <= settings.MAX_REWRITES
        # if nothing matched, is_relevant should be False
        if result.get("relevant_count", 0) == 0:
            assert result.get("is_relevant") is False
    finally:
        # restore original
        if orig_max is None:
            try:
                object.__delattr__(settings, "MAX_REWRITES")
            except Exception:
                pass
        else:
            object.__setattr__(settings, "MAX_REWRITES", orig_max)
