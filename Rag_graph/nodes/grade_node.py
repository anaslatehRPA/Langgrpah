def grade_node(state):
    """
    Grade node with an internal rewrite+retrieve loop.

    This node will check relevance; if not relevant it will call
    `rewrite_query_node` and `retriever_node` in-place and retry, up to
    `MAX_REWRITES` from settings. It mutates `state` and returns it.
    """
    from ..configs.settings import settings
    from .rewrite_query_node import rewrite_query_node
    from .retriever_node import retriever_node

    max_rewrites = getattr(settings, "MAX_REWRITE", 2)
    state.setdefault("rewrite_count", 0)

    def check_relevance():
        retrieved_docs = state.get("retrieved_docs", [])
        query = state.get("query", "").lower()
        docs = state.get("docs", {})
        relevant_count = 0
        for fname in retrieved_docs:
            content = docs.get(fname, "").lower()
            if query in fname.lower() or query in content:
                relevant_count += 1
        # If nothing matched directly, try to interpret query as a project name
        if relevant_count == 0 and retrieved_docs:
            # extract project prefixes from retrieved filenames
            retrieved_projects = set(f.split('/')[0].lower() for f in retrieved_docs if '/' in f)
            # normalize query tokens
            import re
            tokens = re.findall(r"[a-zA-Z0-9_]+", query)
            for proj in retrieved_projects:
                for tok in tokens:
                    if tok and (tok in proj or proj in tok):
                        relevant_count = len([f for f in retrieved_docs if f.lower().startswith(proj)])
                        break
                if relevant_count > 0:
                    break
        state["relevant_count"] = relevant_count
        state["is_relevant"] = True if relevant_count > 0 else False
        return state["is_relevant"]

    # initial check
    is_rel = check_relevance()
    # Privacy-safe debug: log counts and relevance only
    print(f"DEBUG grade_node start: rewrite_count={state.get('rewrite_count', 0)}, is_relevant={is_rel}, relevant_count={state.get('relevant_count',0)}")

    # If not relevant, attempt rewrites and retrievals in-place
    while not is_rel and state.get("rewrite_count", 0) < max_rewrites:
        # rewrite query (increments rewrite_count)
        state = rewrite_query_node(state)
        # rerun retriever to refresh retrieved_docs
        state = retriever_node(state)
        # re-check relevance
        is_rel = check_relevance()
    # Privacy-safe retry log
    print(f"DEBUG grade_node retry: rewrite_count={state.get('rewrite_count', 0)}, is_relevant={is_rel}, relevant_count={state.get('relevant_count',0)}")

    # final status logged (do not print docs content)
    print(f"DEBUG grade_node end: rewrite_count={state.get('rewrite_count', 0)}, is_relevant={state.get('is_relevant')}, relevant_count={state.get('relevant_count')}")
    return state
