from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class State(TypedDict, total=False):
    """
    A TypedDict representing the state carried through the graph.
    Include keys used by nodes so values are preserved by the runtime.
    """
    project_name: str
    query: str
    docs: Dict[str, Any]
    vectorstore: Any
    retrieved_docs: List[str]
    plan_summary: str
    llm_answer: str
    structured_output: Dict[str, Any]
    history: List[Dict[str, Any]]