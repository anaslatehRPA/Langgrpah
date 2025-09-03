import os
from flask import Flask, request, render_template_string
from Rag_graph.nodes.document_loader_node import load_project_documents
from Rag_graph.nodes.retriever_node import retriever_node
from Rag_graph.nodes.grade_node import grade_node
from Rag_graph.nodes.planner_node import planner_node
from Rag_graph.nodes.llm_node import llm_node
from Rag_graph.nodes.answer_re_evaluation_node import answer_re_evaluation_node

app = Flask(__name__)
DATA_ROOT = os.environ.get("DATA_ROOT", "data")

INDEX_HTML = """
<!doctype html>
<title>Project RAG Assistant</title>
<h1>Project RAG Assistant</h1>
<form method=post>
  <textarea name=query rows=4 cols=60 placeholder="Ask about a project..."></textarea><br>
  <input type=submit value=Ask>
</form>
{% if answer %}
<hr>
<h2>Answer</h2>
<pre>{{answer}}</pre>
{% endif %}
"""


def run_query(query: str) -> str:
    state = {"query": query.strip(), "history": []}
    state = load_project_documents(state, DATA_ROOT)
    state = retriever_node(state)
    state = grade_node(state)
    state = planner_node(state)
    state = llm_node(state)
    state = answer_re_evaluation_node(state)
    return state.get("llm_answer", "(no answer)")


@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        q = request.form.get('query', '')
        if q:
            answer = run_query(q)
    return render_template_string(INDEX_HTML, answer=answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False)
