"""Command line interface for the LangGraph agent template."""
import sys
import traceback
from typing import Any, Dict
import click
from Rag_graph.graph import ProjectPlanningGraph


@click.command()
@click.option('--graph-name', default='project_graph', help='Name of the graph to create')
@click.option('--input-text', default='Hello, world!', help='Input text for the graph')
@click.option('--no-llm', is_flag=True, default=False, help='Do not call LLM (hint passed to the workflow)')
@click.option('--timeout', default=0, type=int, help='Optional timeout in seconds (not enforced)')
def main(graph_name: str, input_text: str, no_llm: bool, timeout: int) -> None:
    """Run the LangGraph agent with the specified input."""
    click.echo(f"Creating graph: {graph_name}")

    graph = ProjectPlanningGraph(graph_name)
    compiled_graph = graph.build_and_compile()

    click.echo(f"Running graph with input: {input_text}")
    # prepare input state; pass a hint to skip LLM if requested
    input_state: Dict[str, Any] = {"query": input_text}
    if no_llm:
        input_state["skip_llm"] = True

    try:
        result = compiled_graph.invoke(input_state)
    except Exception as exc:
        click.echo("Error invoking graph:")
        click.echo(str(exc))
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    # Prefer printing the LLM answer if present for readability
    llm_answer = None
    if isinstance(result, dict):
        llm_answer = result.get("llm_answer") or result.get("LLM_ANSWER")

    if no_llm and not llm_answer:
        click.echo("LLM invocation was skipped (no_llm flag). Showing workflow state output:")
        click.echo(str(result))
    else:
        if llm_answer:
            click.echo("\nAgent Response:")
            click.echo(llm_answer)
        else:
            click.echo("\nResult:")
            click.echo(str(result))


if __name__ == '__main__':
    main()  # type: ignore[call-arg]
