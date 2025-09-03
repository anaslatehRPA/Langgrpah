import types
import pytest

from Rag_graph.nodes.answer_re_evaluation_node import answer_re_evaluation_node
from Rag_graph.configs.settings import settings


class DummyLLM:
    def __init__(self, response_text):
        self.response_text = response_text

    def invoke(self, messages):
        # emulate simple invoke
        return self.response_text


def test_reeval_with_llm(monkeypatch):
    state = {
        "llm_answer": "Initial answer without keywords.",
        "plan_summary": "Mitigation plan timeline budget",
        "query": "What are the risks?",
    }
    dummy = DummyLLM("Refined answer including mitigation and timeline and budget.")
    # patch settings.LLM
    monkeypatch.setattr(settings, "LLM", dummy)
    out = answer_re_evaluation_node(state)
    assert out.get("reeval_count", 0) == 1
    assert out.get("needs_reeval") is True or out.get("needs_reeval") is False
    assert "Refined answer" in out["llm_answer"]


def test_reeval_fallback_no_llm():
    state = {
        "llm_answer": "Short answer.",
        "plan_summary": "Mitigation plan timeline budget",
        "query": "What are the risks?",
    }
    # ensure no LLM is configured
    settings.LLM = None
    out = answer_re_evaluation_node(state)
    assert out.get("reeval_count", 0) == 1
    assert out.get("needs_reeval") is True or out.get("needs_reeval") is False
    assert out["llm_answer"].startswith("[Refine to include:")
