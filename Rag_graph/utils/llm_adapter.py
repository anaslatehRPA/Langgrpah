from typing import Any

try:
    # langchain_core may not be available in tests; guard the import
    from langchain_core.messages import HumanMessage
except Exception:
    HumanMessage = None  # type: ignore


def invoke_llm(llm: Any, prompt: str) -> str:
    """
    Normalize calling different LLM adapters used in this project.

    Supports objects with an `invoke(messages)` method (e.g. LangChain-style)
    or simple callables that accept a prompt string. Returns the response
    text or empty string on failure.
    """
    if llm is None:
        return ""

    try:
        # Prefer an `invoke` method taking a list of messages
        if hasattr(llm, "invoke"):
            if HumanMessage is not None:
                msg = HumanMessage(content=prompt)
                res = llm.invoke([msg])
            else:
                # Fallback: pass raw prompt
                res = llm.invoke([prompt])
            if isinstance(res, str):
                return res
            return getattr(res, "content", str(res))

        # If the llm is directly callable
        if callable(llm):
            res = llm(prompt)
            if isinstance(res, str):
                return res
            return getattr(res, "content", str(res))

        # As a last effort, try common alternatives
        if hasattr(llm, "generate"):
            res = llm.generate(prompt)
            if isinstance(res, str):
                return res
            return getattr(res, "content", str(res))

    except Exception:
        # swallow errors and return empty string to let callers fallback
        return ""

    return ""
