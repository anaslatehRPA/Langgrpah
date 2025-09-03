from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from .models.states.state import State
from .configs.settings import settings


class ProjectPlanningGraph:
    """
    Workflow graph for project planning RAG agent.
    """

    def __init__(self, graph_name: str):
        self.graph_name = graph_name
        self.compiled_graph = None

    def build_and_compile(self):
        # Import nodes lazily to avoid top-level side-effects
        from .nodes.document_loader_node import load_project_documents
        from .nodes.retriever_node import retriever_node
        from .nodes.planner_node import planner_node
        from .nodes.llm_node import llm_node
        from .nodes.grade_node import grade_node
        from .nodes.rewrite_query_node import rewrite_query_node
        from .nodes.answer_re_evaluation_node import answer_re_evaluation_node

        workflow = StateGraph(State, input=State)

        # register nodes
        workflow.add_node("document_loader", load_project_documents)
        workflow.add_node("retriever_node", retriever_node)
        workflow.add_node("grade_node", grade_node)
        workflow.add_node("rewrite_query_node", rewrite_query_node)
        workflow.add_node("planner_node", planner_node)
        workflow.add_node("llm_node", llm_node)
        workflow.add_node("answer_re_evaluation_node", answer_re_evaluation_node)

        # Edges: START -> document_loader -> retriever -> grade -> planner
        # rewrite_query_node -> retriever_node (used by grade_node in-place)
        workflow.add_edge(START, "document_loader")
        workflow.add_edge("document_loader", "retriever_node")
        workflow.add_edge("retriever_node", "grade_node")
        # grade node performs in-place rewrite+retrieve loop and then proceeds
        workflow.add_edge("grade_node", "planner_node")
        workflow.add_edge("rewrite_query_node", "retriever_node")
        workflow.add_edge("planner_node", "llm_node")
        # After LLM produces `llm_answer`, run optional answer re-evaluation/refinement
        workflow.add_edge("llm_node", "answer_re_evaluation_node")
        workflow.add_edge("answer_re_evaluation_node", END)

        self.compiled_graph = workflow.compile(name=self.graph_name)
        return self.compiled_graph