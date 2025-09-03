from Rag_graph.nodes.llm_node import llm_node


def test_llm_node_project_list_branch():
    docs = {"Proj_A/readme.md": "x", "ProjB/doc.md": "y"}
    state = {"query": "list projects", "docs": docs, "retrieved_docs": []}
    out = llm_node(state)
    ans = out.get("llm_answer", "")
    # Should contain bullet list lines and at least one project display name
    assert "- " in ans
    assert "Proj A" in ans or "Projb" in ans


def test_llm_node_uses_settings_llm_for_non_list(monkeypatch):
    docs = {"Proj_A/readme.md": "x"}
    state = {"query": "Tell me about Proj_A", "docs": docs, "retrieved_docs": ["Proj_A/readme.md"], "plan_summary": "some plan"}

    class DummyLLM:
        def invoke(self, messages):
            class R:
                content = "DUMMY-RESPONSE"

            return R()

    from Rag_graph.configs.settings import settings as _s
    monkeypatch.setattr(_s, "LLM", DummyLLM())

    out = llm_node(state)
    assert out.get("llm_answer") == "DUMMY-RESPONSE"
