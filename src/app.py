import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from qa_chain import get_qa_chain
from rewriter import rewrite_query

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
CORS(app)

qa = get_qa_chain()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if not question.strip():
        return jsonify({"answer": "⚠ Please enter a valid question."})

    # Rewrite query + send to QA
    rewritten = rewrite_query(question)
    result = qa.invoke({"query": rewritten})

    # Only return the answer
    answer = result.get("result", "⚠ No answer found.")

    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
