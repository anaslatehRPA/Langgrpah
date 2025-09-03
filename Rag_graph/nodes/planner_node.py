def planner_node(state):
    """
    รับ state ที่มี retrieved_docs
    คืนค่า state พร้อม plan_summary (สรุปแผนงาน)
    """
    retrieved_docs = state.get("retrieved_docs", [])
    docs = state.get("docs", {})
    matched_contents = [docs.get(fname, f"[ไม่พบเนื้อหา: {fname}]") for fname in retrieved_docs]
    if matched_contents and any(matched_contents):
        plan_summary = "\n\n".join(matched_contents)
    else:
        # ถ้าไม่มีเนื้อหาที่เกี่ยวข้อง ให้ตอบ default message
        query = state.get("query", "")
        if query.strip() in ["", "สวัสดีครับ", "สวัสดีค่ะ", "hello", "hi"]:
            plan_summary = "สวัสดีครับ ยินดีที่ได้ช่วยเหลือ มีอะไรให้ผมช่วยวางแผนโปรเจคของคุณได้บ้างครับ?"
        else:
            plan_summary = f"ขออภัยครับ ไม่พบข้อมูลที่เกี่ยวข้องกับ '{query}' ในระบบ หากต้องการสอบถามเรื่องอื่น ๆ สามารถพิมพ์คำถามใหม่ได้เลยครับ"
    state["plan_summary"] = plan_summary
    # Privacy-safe debug: print counts and retrieved document names only
    docs = state.get("docs") or {}
    retrieved = state.get("retrieved_docs") or []
    try:
        project_names = sorted(set(p.split('/')[0] for p in docs.keys()))
    except Exception:
        project_names = []
    print(f"DEBUG planner_node: retrieved_count={len(retrieved)}, docs_count={len(docs)}, projects_found={project_names}")
    return state
