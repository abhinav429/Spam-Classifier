# SMS Spam Classifier

A machine learning-powered web application that classifies SMS messages as spam or legitimate (ham) using Natural Language Processing (NLP) and Multinomial Naive Bayes algorithm. Built with Streamlit for an interactive user interface.

## 🎯 Features

- **Real-time Classification**: Instantly classify SMS messages as spam or not spam
- **Confidence Scores**: View prediction confidence percentages for each classification
- **Modern UI/UX**: 
  - Dark/Light mode toggle
  - Responsive design
  - Visual feedback and animations
- **Prediction History**: Track all predictions in a sidebar with statistics
- **Statistics Dashboard**: 
  - Key metrics (spam count, percentage, average confidence)
  - Visual analytics with bar charts
  - Session summary and breakdown
- **Input Validation**: Ensures proper message input before prediction

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Machine Learning**: 
  - Scikit-learn (Multinomial Naive Bayes)
  - NLTK (Natural Language Processing)
- **Text Processing**: 
  - TF-IDF Vectorization
  - Tokenization, Stopword Removal, Stemming
- **Language**: Python 3.11+

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/abhinav429/Spam-Classifier.git
cd Spam-Classifier
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `nltk` - Natural Language Toolkit
- `scikit-learn` - Machine learning library

### 4. Download NLTK Data

The application will automatically download required NLTK data (`punkt_tab` and `stopwords`) on first run. If you encounter issues, you can manually download them:

```python
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
```

## ▶️ Running the Application

### Local Development

1. Make sure you're in the project directory and your virtual environment is activated

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. The application will open automatically in your default web browser at:
   ```
   http://localhost:8501
   ```

4. If it doesn't open automatically, copy the URL from the terminal and paste it into your browser

### Using the Application

1. **Enter a Message**: Type or paste an SMS message in the text area
2. **Click Predict**: Click the "Predict" button to classify the message
3. **View Results**: 
   - See the classification result (Spam/Not Spam)
   - Check the confidence score
   - View statistics in the collapsible dashboard
   - Track history in the sidebar


## 🤖 Model Details

### Algorithm
- **Multinomial Naive Bayes**: A probabilistic classifier that works well with text classification tasks

### Text Preprocessing Pipeline
1. **Lowercasing**: Convert all text to lowercase
2. **Tokenization**: Split text into individual words
3. **Alphanumeric Filtering**: Remove special characters
4. **Stopword Removal**: Remove common English words (the, is, at, etc.)
5. **Stemming**: Reduce words to their root form using Porter Stemmer
6. **Vectorization**: Convert processed text to numerical features using TF-IDF

### Training
The model was trained on a dataset of SMS messages labeled as spam or ham. The training process is documented in `sms-spam-detection.ipynb`.

