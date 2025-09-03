from Rag_graph.utils.llm_adapter import invoke_llm


def test_invoke_llm_with_callable():
    def simple_callable(prompt: str):
        return "callable-response: " + prompt

    out = invoke_llm(simple_callable, "hello")
    assert "callable-response" in out


def test_invoke_llm_with_invoke_method():
    class Resp:
        def __init__(self, content):
            self.content = content

    class LLMObj:
        def invoke(self, messages):
            # messages may be a list; return object with content
            return Resp("invoked-response")

    out = invoke_llm(LLMObj(), "prompt")
    assert out == "invoked-response"


def test_invoke_llm_handles_exceptions():
    class BadLLM:
        def invoke(self, messages):
            raise RuntimeError("boom")

    out = invoke_llm(BadLLM(), "p")
    assert out == ""
