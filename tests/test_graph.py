"""Test graph functionality."""
import pytest
from Rag_graph.graph import ProjectPlanningGraph


def test_graph_creation():
    """Test graph creation."""
    graph = ProjectPlanningGraph("test_graph")
    assert graph.graph_name == "test_graph"
    
    
def test_graph_compilation():
    """Test graph compilation."""
    graph = ProjectPlanningGraph("test_graph")
    compiled_graph = graph.build_and_compile()
    assert compiled_graph is not None


def test_graph_exists():
    """Test that YourGraphName class exists and is importable."""
    assert ProjectPlanningGraph is not None

def test_workflow_all_projects():
    graph = ProjectPlanningGraph("test_graph")
    compiled_graph = graph.build_and_compile()
    input_state = {
        "docs": {},
        "query": "งบประมาณ"
    }
    result = compiled_graph.invoke(input_state)
    # ตรวจสอบว่ามี docs และไม่ error
    assert "docs" in result
