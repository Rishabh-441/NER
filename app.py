from flask import Flask, request, render_template
import spacy
from spacy import displacy
from striprtf.striprtf import rtf_to_text  # Import RTF cleaner

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/entity', methods=['POST', 'GET'])
def entity():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            rtf_content = file.read().decode('utf-8', errors='ignore')
            clean_text = rtf_to_text(rtf_content)  # Convert RTF to plain text

            # Preserve new lines in HTML
            formatted_text = clean_text.replace("\n", "<br>")

            docs = nlp(clean_text)
            html_code = displacy.render(docs, style='ent', page=True)

            return render_template("index.html", html_code=html_code, text=formatted_text)

    return render_template("index.html", html_code="", text="")

if __name__ == '__main__':
    app.run(debug=True)
