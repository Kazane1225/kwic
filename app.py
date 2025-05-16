from flask import Flask, render_template, request, jsonify
import spacy
import spacy.cli
import os
from kwic import kwic_search
from termcolor import colored

app = Flask(__name__)

# ✅ モデルがなければダウンロードして読み込む
try:
    nlp = spacy.load("en_core_web_sm")
except:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        search_type = request.form.get("search_type")
        query = request.form.get("query")
        window = int(request.form.get("window", 5))
        sort_mode = request.form.get("sort_mode")
        attrs = request.form.getlist("attrs")

        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
            print(f"📝 file uploaded: {uploaded_file.filename}")
        else:
            text = request.form.get("text", "")
            print(f"✍️  textarea input: {text[:50]}...")

        print(f"🔍 search_type={search_type}, query={query}, sort={sort_mode}, window={window}")
        doc = nlp(text)
        results = kwic_search(doc, search_type, query, window, color="red", attrs=attrs, sort_mode=sort_mode)
        print(f"✅ hits: {len(results)}")

    return render_template("index.html", results=results)

@app.route("/ajax", methods=["POST"])
def ajax_search():
    search_type = request.form.get("search_type")
    query = request.form.get("query")
    window = int(request.form.get("window", 5))
    sort_mode = request.form.get("sort_mode")
    attrs = request.form.getlist("attrs")

    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    else:
        text = request.form.get("text", "")

    doc = nlp(text)
    results = kwic_search(doc, search_type, query, window, color="red", attrs=attrs, sort_mode=sort_mode)
    return jsonify(results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
