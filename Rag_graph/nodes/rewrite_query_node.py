def rewrite_query_node(state):
    """
    ถ้าไม่พบเอกสารที่เกี่ยวข้อง ให้ปรับ query ใหม่ (เช่น เพิ่ม keyword หรือถามกว้างขึ้น)
    ตัวอย่างนี้: ถ้า relevant_count = 0 จะเพิ่มคำว่า 'สรุป' หรือ 'รายละเอียด' นำหน้า query เดิม
    """
    query = state.get("query", "")
    relevant_count = state.get("relevant_count", 0)
    # ถ้า relevant_count = 0 ให้ปรับ query
    if relevant_count == 0:
        if not query.lower().startswith("สรุป"):
            new_query = f"สรุป {query}"
        else:
            new_query = f"รายละเอียด {query}"
        state["query"] = new_query
    # Always increment rewrite_count to break loop
    prev_count = state.get("rewrite_count", 0)
    state["rewrite_count"] = prev_count + 1
    # Privacy-safe debug: log rewrite counts only
    print(f"DEBUG rewrite_query_node: prev_count={prev_count}, new_count={state['rewrite_count']}")
    return state
