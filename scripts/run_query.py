#!/usr/bin/env python
"""Run a one-shot query against the ProjectPlanningGraph.

Usage:
  python scripts/run_query.py --query "your question here"
"""
import argparse
from Rag_graph.graph import ProjectPlanningGraph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", required=False, default="คุณมีข้อมูล โปรเจคอะไรบ้าง",
                        help="Query to send to the agent (default: ask which projects exist)")
    args = parser.parse_args()

    graph = ProjectPlanningGraph("project_graph")
    compiled = graph.build_and_compile()
    state = {"history": []}
    state["query"] = args.query
    result = compiled.invoke(state)
    llm_answer = result.get("llm_answer", "(no answer)")
    print("\nAGENT RESPONSE:\n")
    print(llm_answer)


if __name__ == "__main__":
    main()
