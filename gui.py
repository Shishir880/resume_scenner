import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Predictor", layout="centered")

st.title("🔍 AI Resume Category Predictor")
st.write("আপনার রিজিউম আপলোড করুন এবং আপনার চাকরির ক্যাটাগরি খুঁজে বের করুন!")

uploaded_file = st.file_uploader("📂 ফাইল আপলোড করুন (PDF, TXT, DOCX, PNG, JPG)", type=["pdf", "txt", "docx", "png", "jpg"])

if uploaded_file is not None:
    with st.spinner("🔄 প্রেডিকশন চলছে..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post("http://127.0.0.1:5000/predict", files=files)

        if response.status_code == 200:
            predicted_category = response.json().get("category")
            st.success(f"✅ আপনার রিজিউম ক্যাটাগরি: **{predicted_category}**")
        else:
            st.error(f"❌ কিছু সমস্যা হয়েছে, আবার চেষ্টা করুন। (Error Code: {response.status_code})")
