import os
import gradio as gr
from Rag_graph.nodes.document_loader_node import load_project_documents
from Rag_graph.nodes.retriever_node import retriever_node
from Rag_graph.nodes.grade_node import grade_node
from Rag_graph.nodes.planner_node import planner_node
from Rag_graph.nodes.llm_node import llm_node
from Rag_graph.nodes.answer_re_evaluation_node import answer_re_evaluation_node

DATA_ROOT = os.environ.get("DATA_ROOT", "data")


def run_query(query: str) -> str:
    # Basic sanitization
    if not query or not isinstance(query, str):
        return "(empty query)"
    if len(query) > 2000:
        return "(query too long)"

    state = {"query": query.strip(), "history": []}
    # Steps of the RAG workflow
    state = load_project_documents(state, DATA_ROOT)
    state = retriever_node(state)
    state = grade_node(state)
    state = planner_node(state)
    state = llm_node(state)
    state = answer_re_evaluation_node(state)

    ans = state.get("llm_answer") or "(no answer)"
    return ans


iface = gr.Interface(
    fn=run_query,
    inputs=gr.Textbox(lines=3, placeholder="ถามเรื่องโปรเจคได้ เช่น 'สรุป Project_Alpha'"),
    outputs=gr.Textbox(label="Agent response"),
    title="Project RAG Assistant",
    description="Local demo: loader → retriever → grade → planner → llm → re-eval",
)

if __name__ == "__main__":
    # Default: localhost only. Set GRADIO_SHARE=true to enable a temporary public link.
    share = os.environ.get("GRADIO_SHARE", "false").lower() in ("1", "true", "yes")
    iface.launch(server_name="0.0.0.0", server_port=7860, share=share)
