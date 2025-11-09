from flask import Flask, render_template, request, jsonify
from app.components.retriever import create_qa_chain
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('prompt', '')
    if not question:
        return jsonify({'answer': "❗Veuillez poser une question."})

    qa_chain = create_qa_chain()
    try:
        response = qa_chain.invoke(question)
        if isinstance(response, dict):
            response = response.get("result") or response.get("answer") or str(response)
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'answer': f"⚠️ Erreur : {str(e)}"})

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("files")
    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"message": f"{len(files)} fichier(s) chargé(s)."})


if __name__ == '__main__':
    app.run(debug=True)
