from Rag_graph.nodes.answer_re_evaluation_node import answer_re_evaluation_node


def test_answer_re_evaluation_with_llm(monkeypatch):
    state = {
        "query": "what about project",
        "plan_summary": "This plan includes schedule deliverable milestone",
        "llm_answer": "A short answer without keywords",
        "docs": {"P/a.md": "x"},
        "retrieved_docs": ["P/a.md"],
    }

    class DummyLLM:
        def invoke(self, messages):
            class R:
                content = "REFINED ANSWER"

            return R()

    from Rag_graph.configs.settings import settings as _s
    monkeypatch.setattr(_s, "LLM", DummyLLM())
    monkeypatch.setattr(_s, "MAX_REEVALS", 1)

    out = answer_re_evaluation_node(state)
    assert out.get("llm_answer") == "REFINED ANSWER"
    assert out.get("reeval_count", 0) == 1


def test_answer_re_evaluation_fallback_no_llm(monkeypatch):
    state = {
        "query": "what about project",
        "plan_summary": "include schedule deliverable milestone",
        "llm_answer": "answer missing keywords",
        "docs": {"P/a.md": "x"},
        "retrieved_docs": ["P/a.md"],
    }
    from Rag_graph.configs.settings import settings as _s
    monkeypatch.setattr(_s, "LLM", None)
    monkeypatch.setattr(_s, "MAX_REEVALS", 1)

    out = answer_re_evaluation_node(state)
    # fallback should prepend a hint
    assert out.get("llm_answer", "").startswith("[Refine to include:")
