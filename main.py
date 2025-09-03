from Rag_graph.graph import ProjectPlanningGraph
import argparse


def run_one_shot(compiled_graph, query: str):
    input_state = {"query": query}
    result = compiled_graph.invoke(input_state)
    # Privacy-safe output: only print the agent's final answer (project names or fallback)
    final = result.get("llm_answer") or result.get("plan_summary") or result.get("query")
    print("Agent Response:\n" + str(final))
    llm_answer = result.get("llm_answer", None)
    print("\nAgent Response:")
    print(llm_answer)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Planning RAG Agent")
    parser.add_argument("--query", "-q", help="One-shot query to run and exit")
    args = parser.parse_args()

    graph = ProjectPlanningGraph("project_graph")
    compiled_graph = graph.build_and_compile()

    if args.query:
        # Non-interactive one-shot
        run_one_shot(compiled_graph, args.query)
    else:
        # Interactive mode with persistent state and history
        print("==== Project Planning RAG Agent ====")
        print("พิมพ์ข้อความสอบถาม (เช่น 'งบประมาณ', 'แผนงาน', 'รายละเอียด') หรือพิมพ์ 'exit'/'quit' เพื่อออก")
        state = {"history": []}
        MAX_HISTORY = 40
        while True:
            try:
                user_query = input("\nQuery: ").strip()
            except EOFError:
                # User sent EOF (Ctrl+D/Ctrl+Z). Exit cleanly without traceback.
                print("\nEOF received, exiting")
                # Ensure a clean exit with code 0
                import sys
                sys.exit(0)
            except KeyboardInterrupt:
                # User pressed Ctrl+C. Treat it as a polite exit command.
                print("\nKeyboard interrupt, exiting")
                import sys
                sys.exit(0)

            if not user_query:
                # ignore empty input and prompt again
                continue

            # Special REPL commands
            if user_query.lower() in ("exit", "quit"):
                print("ออกจากระบบแล้ว")
                break

            if user_query.lower() in ("reload", "reindex"):
                # Re-scan the data/ directory and (re)build embeddings/vectorstore if possible
                try:
                    from Rag_graph.nodes.document_loader_node import load_project_documents
                    state = load_project_documents(state, data_root="data")
                    docs = state.get("docs", {}) or {}
                    projects = sorted(set(k.split('/')[0] for k in docs.keys()))
                    print(f"Reindexed {len(docs)} documents across {len(projects)} projects")
                except Exception as e:
                    print(f"Failed to reload documents: {e}")
                continue

            if user_query.lower() in ("list", "list projects", "projects"):
                docs = state.get("docs", {}) or {}
                projects = sorted(set(k.split('/')[0] for k in docs.keys()))
                if not projects:
                    print("No projects found (try 'reload' to rescan the data folder)")
                else:
                    print("Projects found:")
                    for p in projects:
                        print(" - " + p)
                continue

            # Append user turn to history
            state.setdefault("history", []).append({"role": "user", "content": user_query})
            # Trim history to keep memory bounded
            if isinstance(state["history"], list) and len(state["history"]) > MAX_HISTORY:
                state["history"] = state["history"][-MAX_HISTORY:]

            # Add query to state for nodes
            state["query"] = user_query

            try:
                result = compiled_graph.invoke(state)
            except Exception as e:
                # Don't crash the REPL: show a helpful message and continue
                print(f"\nAgent encountered an error: {e}")
                # Record the failure as the agent response so the history remains consistent
                llm_answer = f"(agent error) {e}"
                state.setdefault("history", []).append({"role": "agent", "content": llm_answer})
                continue

            llm_answer = result.get("llm_answer", None)
            if llm_answer is None:
                llm_answer = "(no answer)"

            print("\nAgent Response:")
            print(llm_answer)

            # Append agent turn to history
            state.setdefault("history", []).append({"role": "agent", "content": llm_answer or ""})
