def retriever_node(state):
    """
    รับ state ที่มี docs และ query
    คืนค่า state พร้อม retrieved_docs (list ของเนื้อหาที่เกี่ยวข้อง)
    """
    query = state.get("query", "")
    vectorstore = state.get("vectorstore", None)

    docs = state.get("docs", {}) or {}
    query_lower = query.lower()

    # If no vectorstore (e.g., running without embeddings/credentials), fall back to filename/content search
    if not vectorstore:
        # Exact substring match (case-insensitive)
        filename_matches = [fname for fname in docs.keys() if query_lower in fname.lower()]
        # Fuzzy match using difflib if no exact match
        if not filename_matches:
            import difflib
            # Get close matches for query against filenames
            close_fnames = difflib.get_close_matches(query, list(docs.keys()), n=5, cutoff=0.6)
            filename_matches = close_fnames
        if filename_matches:
            state["retrieved_docs"] = filename_matches
            return state
        # content search fallback (case-insensitive)
        keyword_matches = [fname for fname, content in docs.items() if query_lower in str(content).lower()]
        # Fuzzy match in content if no exact match
        if not keyword_matches:
            import difflib
            for fname, content in docs.items():
                # Get close matches for query against each line in content
                lines = str(content).splitlines()
                matches = difflib.get_close_matches(query, lines, n=1, cutoff=0.6)
                if matches:
                    keyword_matches.append(fname)
        state["retrieved_docs"] = keyword_matches
        return state

    # With a vectorstore available, prefer semantic search but still keep fallbacks
    try:
        results = vectorstore.similarity_search(query, k=3)
    except Exception:
        results = []

    matched_files = [getattr(r, 'metadata', {}).get("source") for r in results if getattr(r, 'metadata', {}).get("source")]

    # Fallback 1: search filenames for query
    if not matched_files:
        filename_matches = [fname for fname in docs.keys() if query_lower in fname.lower()]
        if filename_matches:
            matched_files = filename_matches

    # Fallback 2: search content if still no match
    if not matched_files:
        keyword_matches = [fname for fname, content in docs.items() if query_lower in str(content).lower()]
        matched_files = keyword_matches

    # Fallback 3: if still no matches, try to detect a project name in the query
    # and return all files under that project folder (useful when filenames are structured
    # as 'Project_Name/filename'). This helps queries like "Project Alpha" match files.
    if not matched_files:
        import re
        # extract tokens from query
        tokens = [t.lower() for t in re.findall(r"[a-zA-Z0-9_]+", query_lower)]
        if tokens:
            # gather project prefixes
            project_prefixes = set(p.split('/')[0] for p in docs.keys() if '/' in p)
            matched_projects = []
            for proj in project_prefixes:
                pl = proj.lower()
                for tok in tokens:
                    if tok in pl or pl in tok:
                        matched_projects.append(proj)
                        break
            if matched_projects:
                # return all files that start with any matched project prefix
                proj_files = [f for f in docs.keys() if any(f.startswith(p + '/') for p in matched_projects)]
                if proj_files:
                    matched_files = proj_files

    state["retrieved_docs"] = matched_files
    return state
