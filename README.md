# Resume Category Predictor

This project is a **Resume Category Predictor** that uses Machine Learning to classify resumes into different job categories. It supports multiple file formats including **PDF, TXT, DOCX, PNG, and JPG**.

## Features
- Extracts text from resumes (PDF, DOCX, TXT, Images)
- Cleans and processes text using **TF-IDF Vectorization**
- Predicts job category using a **pre-trained machine learning model**
- Provides an API endpoint for predictions
- Comes with a **Streamlit frontend** for easy usage

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/Shishir880/resume_scenner.git
   cd YOUR_REPO_NAME
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure **Tesseract OCR** is installed for image text extraction:
   - Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: Install via package manager (e.g., `sudo apt install tesseract-ocr`)

## Usage

### Running the API (Flask)
```bash
python api.py
```
The API will run at `http://127.0.0.1:5000`

### Running the Streamlit App
```bash
streamlit run app.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Upload a resume and get job category prediction |

### Example Request
```python
import requests
files = {'file': open('resume.pdf', 'rb')}
response = requests.post('http://127.0.0.1:5000/predict', files=files)
print(response.json())
```

## Model & Data
- **Model:** Trained using Scikit-Learn (TF-IDF + Classifier)
- **Data:** Resume dataset with labeled job categories
- **Files Used:**
  - `finalized_model_v2.pkl` (Trained Model)
  - `tfidf.pkl` (TF-IDF Vectorizer)
  - `jobs_category.pkl` (Category Mapping)

## Contributing
Feel free to submit issues or pull requests! 🚀

## License
This project is **MIT Licensed**.

