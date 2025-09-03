from ..configs.settings import settings
from Rag_graph.prompts.prompts import PROJECT_ASSISTANT_PROMPT, REEVAL_PROMPT
from Rag_graph.utils.llm_adapter import invoke_llm


def answer_re_evaluation_node(state):
    """
    After the LLM produces `state['llm_answer']`, this node performs lightweight
    re-evaluation and optional refinement passes. It's intentionally simple and
    local (no external API calls) so tests remain deterministic.

    Behavior:
    - If `state['llm_answer']` is empty, no-op.
    - If `state['plan_summary']` exists and `state['llm_answer']` does not
      reference obvious keywords from `plan_summary`, mark `state['needs_reeval']`
      and attempt up to `settings.MAX_REEVALS` re-evaluations by prefacing the
      answer with a short clarification line.
    - Increment `state['reeval_count']` for visibility.
    """
    answer = state.get("llm_answer", "") or ""
    plan = state.get("plan_summary", "") or ""
    state.setdefault("reeval_count", 0)

    # Simple heuristic: if plan_summary has a short keyword that isn't in the answer,
    # request a small refinement.
    if not answer:
        return state

    if not plan:
        return state

    # pick up to three keywords from plan (split by whitespace, filter short words)
    import re

    tokens = [t.lower() for t in re.findall(r"[\w]{4,}", plan)]
    keywords = tokens[:3]

    missing = [k for k in keywords if k and k not in answer.lower()]
    if missing and state.get("reeval_count", 0) < getattr(settings, "MAX_REEVALS", 1):
        # Tag for calling code / logs that we will re-evaluate
        prev = state.get("reeval_count", 0)
        state["reeval_count"] = prev + 1
        state["needs_reeval"] = True

        # If an LLM instance is configured, call it to produce a refined answer.
        llm = getattr(settings, "LLM", None)
        prompt = REEVAL_PROMPT.format(
            context=plan,
            question=(state.get("query", "")),
            missing=", ".join(missing),
        )
        if llm is not None:
            refined = invoke_llm(llm, prompt)
            if refined:
                state["llm_answer_original"] = answer
                state["llm_answer"] = refined
            else:
                # adapter failed; fallback to hint prepend
                hint = f"[Refine to include: {', '.join(missing)}] "
                state["llm_answer"] = hint + answer
        else:
            # No LLM configured: fallback to lightweight local hint
            hint = f"[Refine to include: {', '.join(missing)}] "
            state["llm_answer"] = hint + answer
    else:
        state["needs_reeval"] = False

    # Privacy-safe debug
    if getattr(settings, "DEBUG", False):
        docs = state.get("docs") or {}
        retrieved = state.get("retrieved_docs") or []
        try:
            project_names = sorted(set(p.split('/')[0] for p in docs.keys()))
        except Exception:
            project_names = []
        print(f"DEBUG answer_re_evaluation_node: reeval_count={state.get('reeval_count',0)}, needs_reeval={state.get('needs_reeval')}, projects_found={project_names}")

    return state
