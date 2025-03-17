from flask import Flask, request, jsonify
import PyPDF2
import docx
import pytesseract
from PIL import Image
import joblib
import re

app = Flask(__name__)

# মডেল এবং TF-IDF লোড
loaded_model = joblib.load("finalized_model_v2.pkl")
loaded_tfidf = joblib.load("tfidf.pkl")
loaded_jobs = joblib.load("jobs_category.pkl")

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = text.lower()
    return text

def extract_text_from_file(file):
    """Extracts text from uploaded PDF, TXT, DOCX, or image files."""
    text = ""
    try:
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        elif file.filename.endswith('.txt'):
            text = str(file.read(), "utf-8")
        elif file.filename.endswith('.docx'):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"❌ Error extracting text: {str(e)}")
        text = ""
    return text

@app.route('/predict', methods=['POST'])
def predict_resume_category():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    resume_text = extract_text_from_file(file)
    if not resume_text:
        return jsonify({'error': 'Could not extract text'}), 400
    cleaned_resume = clean_text(resume_text)
    tfidf_vec_data = loaded_tfidf.transform([cleaned_resume])
    prediction = loaded_model.predict(tfidf_vec_data)[0]
    reverse_job_dict = {v: k for k, v in loaded_jobs.items()}
    category = reverse_job_dict.get(prediction, "Unknown")
    return jsonify({'category': category})

if __name__ == '__main__':
    app.run(debug=True)