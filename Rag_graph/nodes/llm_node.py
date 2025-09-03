import os
from ..configs.settings import settings
from Rag_graph.prompts.prompts import PROJECT_ASSISTANT_PROMPT
from Rag_graph.utils.llm_adapter import invoke_llm


def llm_node(state):
    """
    รับ state ที่มี plan_summary
    คืนค่า state พร้อม llm_answer
    """
    plan_summary = state.get("plan_summary", "")
    user_query = state.get("query", "สวัสดีครับ มีอะไรให้ช่วย?")
    history = state.get("history", [])
    history_text = ""
    if isinstance(history, list) and history:
        parts = []
        for item in history[-10:]:
            role = item.get("role", "user")
            content = item.get("content", "")
            parts.append(f"{role}: {content}")
        history_text = "\n".join(parts)
    # Combine history, plan_summary, and the user query into context for the prompt
    combined_context = ""
    if history_text:
        combined_context += history_text + "\n\n"
    if plan_summary:
        combined_context += plan_summary
    # Decide whether this is a request to list projects or a request about a specific project.
    qlow = (user_query or "").lower()
    project_list_triggers = ["มีโปรเจค", "โปรเจคอะไร", "projects", "what projects", "list projects", "มีโครงการ"]
    docs = state.get("docs", {}) or {}
    projects = sorted({k.split('/')[0] for k in docs.keys() if '/' in k or k})
    # If the query mentions a specific project name or asks for a summary/detail, prefer the normal path
    mentions_project = False
    try:
        proj_names_normalized = [p.replace('_', ' ').replace('-', ' ').lower() for p in projects]
        # create short aliases (drop 'project' prefix) and last token
        aliases = set()
        for pn in proj_names_normalized:
            aliases.add(pn)
            short = pn.replace('project ', '').strip()
            aliases.add(short)
            parts = short.split()
            if parts:
                aliases.add(parts[-1])
        # check if any alias appears as a word in the query
        import re
        q_words = set(re.findall(r"[\w]+", qlow))
        for a in aliases:
            if not a:
                continue
            for token in re.findall(r"[\w]+", a):
                if token in q_words:
                    mentions_project = True
                    break
            if mentions_project:
                break
    except Exception:
        mentions_project = False
    asks_for_summary = any(tok in qlow for tok in ("สรุป", "สรุปให้", "รายละเอียด", "summary", "สรุปหน่อย", "สรุปให้ผม", "สรุปให้ผมที"))

    if any(trigger in qlow for trigger in project_list_triggers) and not mentions_project and not asks_for_summary:
        projects = projects
        lines = []
        import re
        for p in projects:
            display = re.sub(r'project[_\s-]*', '', p, flags=re.I)
            display = display.replace('_', ' ').replace('-', ' ').strip()
            if not display:
                display = p
            display = " ".join([w.upper() if w.isupper() else w.capitalize() for w in display.split()])
            lines.append(f"- {display}")
        if lines:
            state["llm_answer"] = "รายชื่อโปรเจคที่โปรแกรมพบ:\n" + "\n".join(lines)
        else:
            state["llm_answer"] = "ผมยังไม่พบโปรเจคในโฟลเดอร์ data/ — พิมพ์ 'reload' เพื่อสแกนใหม่"
        # Privacy-safe debug: log only counts and project names
        docs = state.get("docs") or {}
        retrieved = state.get("retrieved_docs") or []
        try:
            project_names = sorted(set(p.split('/')[0] for p in docs.keys()))
        except Exception:
            project_names = []
        if getattr(settings, "DEBUG", False):
            print(f"DEBUG llm_node: retrieved_count={len(retrieved)}, docs_count={len(docs)}, projects_found={project_names}")
        return state

    google_api_key = getattr(settings, "GOOGLE_API_KEY", None)
    adc_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    # Prefer pre-initialized settings.LLM if available (helps tests and DI)
    pre_llm = getattr(settings, "LLM", None)
    prompt = PROJECT_ASSISTANT_PROMPT.format(
        context=combined_context,
        question=user_query,
    )
    if pre_llm is not None:
        # Use adapter to call LLM uniformly
        response_text = invoke_llm(pre_llm, prompt)
        state["llm_answer"] = response_text if response_text else plan_summary
        # Privacy-safe debug for fallback path
        docs = state.get("docs") or {}
        retrieved = state.get("retrieved_docs") or []
        try:
            project_names = sorted(set(p.split('/')[0] for p in docs.keys()))
        except Exception:
            project_names = []
        if getattr(settings, "DEBUG", False):
            print(f"DEBUG llm_node fallback: retrieved_count={len(retrieved)}, docs_count={len(docs)}, projects_found={project_names}")
        return state

    # If Google client is available and credentials present, create it
    try:
        # If a Google client is available and credentials present, create it
        from langchain_google_genai import ChatGoogleGenerativeAI
        if (google_api_key or adc_path):
            model_name = getattr(settings, "LLM_MODEL_NAME", "gemini-2.5-pro")
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=google_api_key)
            response_text = invoke_llm(llm, prompt)
            state["llm_answer"] = response_text if response_text else plan_summary
            # Final privacy-safe debug before returning
            docs = state.get("docs") or {}
            retrieved = state.get("retrieved_docs") or []
            try:
                project_names = sorted(set(p.split('/')[0] for p in docs.keys()))
            except Exception:
                project_names = []
            if getattr(settings, "DEBUG", False):
                print(f"DEBUG llm_node end: retrieved_count={len(retrieved)}, docs_count={len(docs)}, projects_found={project_names}")
            return state
    except Exception:
        # fall through to fallback
        pass
        # Final privacy-safe debug before returning
        docs = state.get("docs") or {}
        retrieved = state.get("retrieved_docs") or []
        try:
            project_names = sorted(set(p.split('/')[0] for p in docs.keys()))
        except Exception:
            project_names = []
        if getattr(settings, "DEBUG", False):
            print(f"DEBUG llm_node end: retrieved_count={len(retrieved)}, docs_count={len(docs)}, projects_found={project_names}")
        return state

    # Fallback: no LLM available — respond with a helpful local fallback
    fallback = "(LLM not available) Here is a brief plan based on retrieved context:\n" + (plan_summary or user_query)
    state["llm_answer"] = fallback if fallback else plan_summary
    if getattr(settings, "DEBUG", False):
        print("DEBUG llm_node state:", state)
    return state