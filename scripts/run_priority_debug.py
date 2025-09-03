from Rag_graph.graph import ProjectPlanningGraph
from Rag_graph.nodes.document_loader_node import load_project_documents
import json, pprint

if __name__ == '__main__':
    g = ProjectPlanningGraph('g')
    compiled = g.build_and_compile()
    state = {}
    state = load_project_documents(state, 'data')
    state['query'] = 'ตอนนี้คุณคิดว่าโปรเจคไหนควรทำให้เสร็จเร็วๆ'
    result = compiled.invoke(state)
    print('LLM ANSWER:\n')
    print(result.get('llm_answer'))
    print('\nstructured_output raw repr:')
    so = result.get('structured_output', None)
    print('type:', type(so))
    print('repr:', repr(so))
    print('\npretty json dump (if possible):')
    try:
        print(json.dumps(so, ensure_ascii=False, indent=2))
    except Exception as e:
        print('json dump failed:', e)
    print('\nfull result keys:')
    print(list(result.keys()))
