# LangGraph Agent Template

A template for building LangGraph AI agents with Poetry packaging.

## Installation

### From PyPI (when published)
```bash
pip install langgraph-agent-template
```

### For Development
```bash
git clone <your-repo-url>
cd langgraph-agent-template
poetry install
```

### With PostgreSQL support
```bash
poetry install --extras postgres
```

## Quick Start

```python
from your_graph_name import YourGraphName

# Initialize your graph
graph = YourGraphName("my_graph")
compiled_graph = graph.create_graph()

# Use your graph
result = compiled_graph.invoke({"input": "your input"})
```

## 🛠️ Customization Guide

### 1. Configure Settings (`your_graph_name/configs/settings.py`)

Modify the settings class for your specific needs:
- Add custom API URLs and authentication keys
- Configure LLM parameters (model, temperature, max tokens)
- Set database connections and pool sizes  
- Define environment-specific settings

Update your `.env` file with actual values for all settings.

### 2. Define States (`your_graph_name/models/states/state.py`)

Customize the state structure to match your workflow data requirements:

**What to customize:**
- Input/output fields for your specific domain
- Processing intermediate fields (analysis results, parsed data, etc.)
- Metadata and tracking fields (timestamps, node history, etc.)
- Error handling fields (error messages, retry counts, etc.)
- Context and history fields (conversation, user preferences, etc.)

**Example state structure:**
```python
class State(TypedDict):
    # Core input/output
    user_query: str
    final_response: str
    
    # Domain-specific fields
    document_content: Optional[str]
    extracted_entities: Optional[List[Dict[str, Any]]]
    classification_result: Optional[str]
    confidence_scores: Optional[Dict[str, float]]
    
    # Processing metadata
    processing_steps: List[str]
    current_node: str
    retry_count: int
    
    # Context preservation
    session_id: Optional[str]
    user_preferences: Optional[Dict[str, Any]]
    conversation_context: Optional[List[Dict[str, str]]]
```

### 3. Create Structured Outputs (`your_graph_name/models/structured_output/`)

Define Pydantic models for consistent, validated outputs:

**What to create:**
- Domain-specific output models for your use case
- Validation rules and constraints using Pydantic validators
- Nested models for complex hierarchical data
- Enum classes for controlled vocabularies

**Example files to create:**
- `classification_output.py` - For categorization and labeling results
- `extraction_output.py` - For entity and data extraction results
- `generation_output.py` - For content generation and text outputs
- `search_output.py` - For search and information retrieval results
- `analysis_output.py` - For analytical processing results

**Don't forget:** Update the `__init__.py` file to export your new models:
```python
from .your_new_model import YourNewModel, YourEnum
__all__ = ["YourNewModel", "YourEnum", ...]
```

### 4. Add Tools (`your_graph_name/tools/tool_box`)

Create tool functions in `tool_box` and organize them in `tool_index.py`:

**Step A: Create tools in `tool_box`**

**Example tool structure:**
```python
from langchain_core.tools import tool

@tool
def your_custom_tool(input_param: str, config_param: int = 5) -> Dict[str, Any]:
    """
    Description of what your tool does.
    
    Args:
        input_param: Description of input
        config_param: Configuration parameter with default
    
    Returns:
        Dictionary with results and metadata
    """
    try:
        # Your tool implementation here
        result = process_input(input_param)
        
        return {
            "success": True,
            "result": result,
            "metadata": {"processing_time": 0.1}
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Step B: Register tools in `tool_index.py`**

**Example tool registration:**
```python
from .tool_box.your_tool import your_tool_name

all_tools = [
    your_tool_name,
    # ! Add more tools here
]

tools_by_name = {tool.name: tool for tool in all_tools}
```

### 5. Add Prompts (`your_graph_name/prompts/prompts.py`)

Create prompt templates for different use cases:

**What to add:**
- System prompts for different node types (analysis, generation, routing)
- Task-specific prompts with variable placeholders
- Few-shot examples for complex tasks
- Chain-of-thought prompts for reasoning tasks
- Domain-specific instruction templates

**Example prompt templates:**
```python
# System prompts for different capabilities
SYSTEM_ANALYST_PROMPT = """
You are an expert analyst. Analyze the given input and provide:
1. Key insights and patterns
2. Confidence scores for your analysis  
3. Recommendations for next steps
Format your response as structured JSON.
"""

CONTENT_GENERATOR_PROMPT = """
You are a professional content creator. Generate high-quality content based on:
- Input request: {request}
- Target style: {style}
- Target audience: {audience}
- Content length: {length}

Ensure the content is engaging, accurate, and appropriate.
"""

# Task-specific prompts with examples
CLASSIFICATION_PROMPT = """
Classify the following text into one of these categories: {categories}

Examples:
{examples}

Text to classify: {text}
Classification:
"""

EXTRACTION_PROMPT = """
Extract the following entities from the text:
- {entity_types}

Text: {text}
Extracted entities (JSON format):
"""
```

**Prompt organization tips:**
- Group related prompts together
- Use descriptive names with clear purposes
- Include variable placeholders for dynamic content
- Add comments explaining when to use each prompt

### 6. Create Node Files (`your_graph_name/nodes/`)

Create node files for different processing steps in your workflow:

**Example node file structure:**
```python
from ..models.states.state import State
from ..prompts.prompts import EXAMPLE_PROMPT
from langchain.prompts import PromptTemplate
from ..configs.settings import settings

def your_node_name(state: State) -> State:
    """
    A function node
    """
    # ! Define your node logic here
    text_input = state.get("text_input", "")
    # For example, you can use the EXAMPLE_PROMPT to generate an answer
    system_prompt = PromptTemplate.from_template(EXAMPLE_PROMPT)
    # Call your model here to get the answer
    chain = system_prompt | settings.LLM
    # Generate the answer using the model
    result = chain({"text_input": text_input})
    
    # Return the answer
    return {"answer": result["content"]}
```

### 7. Create Graph Workflow (`your_graph_name/graph.py`)

Configure nodes and edges in your main graph class:

**Step A: Import your nodes**
```python
from .nodes.your_input_node import your_input_node
from .nodes.your_analysis_node import your_analysis_node
from .nodes.your_decision_node import your_decision_node
from .nodes.your_output_node import your_output_node
```

**Step B: Add nodes to the graph**
```python
def _build_graph(self):
    workflow = StateGraph(State, input=State)
    
    # Add your custom nodes
    workflow.add_node("input_processing", your_input_node)
    workflow.add_node("analysis", your_analysis_node)
    workflow.add_node("decision", your_decision_node)
    workflow.add_node("output_generation", your_output_node)
```

**Step C: Define edges and flow**
```python
    # Simple sequential edges
    workflow.add_edge(START, "input_processing")
    workflow.add_edge("input_processing", "analysis")
    workflow.add_edge("analysis", "decision")
    workflow.add_edge("output_generation", END)
    
    # Conditional edges for routing
    workflow.add_conditional_edges(
        "decision",
        your_decision_node,  # Router function
        {
            "generate_output": "output_generation",
            "retry_analysis": "analysis",
            "end_process": END
        }
    )
```

**Common graph patterns:**
- **Linear flow**: START → Node1 → Node2 → Node3 → END
- **Conditional routing**: Use router nodes to direct flow based on state
- **Parallel processing**: Multiple nodes can process simultaneously
- **Retry loops**: Route back to previous nodes on errors
- **Subgraphs**: Create reusable sub-workflows

## Development Workflow

### Setup
```bash
poetry install --with dev,docs
poetry run pre-commit install
```

### Testing
```bash
poetry run pytest
```

### Code Quality
```bash
poetry run black .
poetry run isort .
poetry run flake8
poetry run mypy
```
