import streamlit as st
import pickle
import re
import PyPDF2
import docx
import pytesseract
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model, TF-IDF vectorizer, and job categories
loaded_model = pickle.load(open('finalized_model_v2.pkl', 'rb'))
loaded_tfidf = pickle.load(open('tfidf.pkl', 'rb'))
loaded_jobs = pickle.load(open('jobs_category', 'rb'))

def clean_text(text):
    """Cleans resume text by removing URLs, special characters, and extra spaces."""
    text = re.sub('http\S+\s*', ' ', text)  # remove URLs
    text = re.sub('RT|cc', ' ', text)  # remove RT and cc
    text = re.sub('#\S+', '', text)  # remove hashtags
    text = re.sub('@\S+', ' ', text)  # remove mentions
    text = re.sub('[%s]' % re.escape("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"), ' ', text)  # remove punctuations
    text = re.sub(r'[^\x00-\x7f]', r' ', text)  # remove non-ASCII characters
    text = re.sub('\s+', ' ', text).strip()  # remove extra whitespace
    return text

def extract_text_from_file(uploaded_file):
    """Extracts text from uploaded PDF, TXT, DOCX, or image files."""
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    elif uploaded_file.type == "text/plain":
        text = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.type in ["image/png", "image/jpeg"]:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
    else:
        text = ""
    return text

def predict_resume_category(resume_text):
    """Predicts the job category of a given resume text."""
    cleaned_resume = clean_text(resume_text)
    tfidf_vec_data = loaded_tfidf.transform([cleaned_resume])
    prediction = loaded_model.predict(tfidf_vec_data)[0]
    reverse_job_dict = {v: k for k, v in loaded_jobs.items()}
    return reverse_job_dict.get(prediction, "Unknown")

# Streamlit UI
st.title("AI Resume Category Predictor")
st.write("Upload your resume (PDF, TXT, DOCX, PNG, JPG) to predict the job category.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt", "docx", "png", "jpg"])

if uploaded_file is not None:
    resume_text = extract_text_from_file(uploaded_file)
    if resume_text:
        predicted_category = predict_resume_category(resume_text)
        st.subheader("Predicted Job Category:")
        st.success(predicted_category)
    else:
        st.error("Could not extract text from the file. Please try another file.")