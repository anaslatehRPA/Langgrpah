from Rag_graph.graph import ProjectPlanningGraph
from Rag_graph.nodes.document_loader_node import load_project_documents
import json

if __name__ == '__main__':
    g = ProjectPlanningGraph('g')
    compiled = g.build_and_compile()
    state = {}
    state = load_project_documents(state, 'data')
    state['query'] = 'ตอนนี้คุณคิดว่าโปรเจคไหนควรทำให้เสร็จเร็วๆ'
    result = compiled.invoke(state)
    print('LLM ANSWER:\n')
    print(result.get('llm_answer'))
    print('\nSTRUCTURED_OUTPUT:\n')
    print(json.dumps(result.get('structured_output', {}), ensure_ascii=False, indent=2))
