import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import ssl
from datetime import datetime
import html

# Fix SSL issues for NLTK
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# Session state initialization
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

col1, col2 = st.columns([1, 0.1])
with col2:
    dark_mode = st.toggle("🌙", value=st.session_state.dark_mode, help="Toggle dark mode")
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

if st.session_state.dark_mode:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stApp > header {
            background-color: #0e1117;
        }
        .main .block-container {
            background-color: #0e1117;
            color: #fafafa;
        }
        h1, h2, h3 {
            color: #fafafa;
        }
        .stTextArea > div > div > textarea {
            background-color: #262730;
            color: #fafafa;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #1f2937;
        }
        .main .block-container {
            background-color: #ffffff;
            color: #1f2937;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1f2937;
        }
        label {
            color: #374151;
            font-weight: 500;
        }
        .stTextArea > div > div > textarea {
            background-color: #ffffff;
            color: #1f2937;
            border: 1px solid #d1d5db;
        }
        .stTextArea > div > div > textarea:focus {
            border-color: #3b82f6;
        }
        .stButton > button {
            background-color: #2563eb;
            color: #ffffff;
            border: none;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #1d4ed8;
        }
        p, div, span {
            color: #1f2937;
        }
        /* Sidebar styling for light mode */
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        .css-1d391kg h2,
        .css-1d391kg h3 {
            color: #1e40af !important;
        }
        /* Total metric label - grey */
        section[data-testid="stSidebar"] div[data-testid="column"]:first-of-type div[data-testid="stMetricLabel"],
        section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(1) div[data-testid="stMetricLabel"] {
            color: #6b7280 !important;
        }
        /* Spam metric label - red */
        section[data-testid="stSidebar"] div[data-testid="column"]:last-of-type div[data-testid="stMetricLabel"],
        section[data-testid="stSidebar"] div[data-testid="column"]:nth-child(2) div[data-testid="stMetricLabel"] {
            color: #dc2626 !important;
        }
        /* Metric values */
        section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {
            color: #1f2937 !important;
        }
        /* Toggle button styling */
        div[data-testid="stToggle"] label {
            color: #374151 !important;
        }
        /* Toggle slider */
        div[data-testid="stToggle"] button[role="switch"],
        div[data-testid="stToggle"] button {
            background-color: #4b5563 !important;
            border-color: #4b5563 !important;
        }
        div[data-testid="stToggle"] button[aria-checked="true"] {
            background-color: #1f2937 !important;
            border-color: #1f2937 !important;
        }
        div[data-testid="stToggle"] button[aria-checked="false"] {
            background-color: #4b5563 !important;
            border-color: #4b5563 !important;
        }
        section[data-testid="stSidebar"] {
            color: #1f2937;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    if input_sms.strip():
        transformed_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transformed_sms])
        result = model.predict(vector_input)[0]
        
        probabilities = model.predict_proba(vector_input)[0]
        confidence = max(probabilities) * 100
        current_confidence = round(confidence, 2)
        
        prediction_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'message': input_sms,
            'result': 'Spam' if result == 1 else 'Not Spam',
            'confidence': current_confidence,
            'id': len(st.session_state.prediction_history)
        }
        st.session_state.prediction_history.insert(0, prediction_entry)
        
        if len(st.session_state.prediction_history) > 15:
            st.session_state.prediction_history = st.session_state.prediction_history[:15]
        
        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")
        
        if st.session_state.prediction_history:
            with st.expander("View Statistics Dashboard", expanded=False):
                total_predictions = len(st.session_state.prediction_history)
                spam_count = sum(1 for entry in st.session_state.prediction_history if entry['result'] == 'Spam')
                ham_count = total_predictions - spam_count
                spam_percentage = (spam_count / total_predictions * 100) if total_predictions > 0 else 0
                avg_confidence = sum(entry['confidence'] for entry in st.session_state.prediction_history) / total_predictions
                
                st.markdown("### Key Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Current Confidence",
                        f"{current_confidence}%",
                        help="Confidence score for the latest prediction"
                    )
                
                with col2:
                    st.metric(
                        "Spam Count",
                        spam_count,
                        help="Total spam predictions in current session"
                    )
                
                with col3:
                    st.metric(
                        "Spam Percentage",
                        f"{spam_percentage:.1f}%",
                        help="Percentage of spam predictions"
                    )
                
                with col4:
                    st.metric(
                        "Avg Confidence",
                        f"{avg_confidence:.1f}%",
                        help="Average confidence score across all predictions"
                    )
                
                st.divider()
                
                st.markdown("### Visual Analytics")
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("**Prediction Distribution**")
                    max_count = max(spam_count, ham_count) if max(spam_count, ham_count) > 0 else 1
                    spam_width = (spam_count / max_count * 100) if max_count > 0 else 0
                    ham_width = (ham_count / max_count * 100) if max_count > 0 else 0
                    
                    st.markdown(f"""
                        <div style="margin: 20px 0;">
                            <div style="margin-bottom: 10px;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                    <span style="color: #dc2626; font-weight: 600;">Spam</span>
                                    <span style="color: {'#d1d5db' if st.session_state.dark_mode else '#4b5563'};">{spam_count}</span>
                                </div>
                                <div style="background-color: {'#374151' if st.session_state.dark_mode else '#e5e7eb'}; height: 25px; border-radius: 5px; overflow: hidden;">
                                    <div style="background-color: #dc2626; height: 100%; width: {spam_width}%; transition: width 0.3s;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                    <span style="color: #16a34a; font-weight: 600;">Not Spam</span>
                                    <span style="color: {'#d1d5db' if st.session_state.dark_mode else '#4b5563'};">{ham_count}</span>
                                </div>
                                <div style="background-color: {'#374151' if st.session_state.dark_mode else '#e5e7eb'}; height: 25px; border-radius: 5px; overflow: hidden;">
                                    <div style="background-color: #16a34a; height: 100%; width: {ham_width}%; transition: width 0.3s;"></div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.caption(f"Spam: {spam_count} ({spam_percentage:.1f}%) | Not Spam: {ham_count} ({100-spam_percentage:.1f}%)")
                
                with chart_col2:
                    st.markdown("**Confidence Score Distribution**")
                    confidence_ranges = {
                        '0-50%': sum(1 for e in st.session_state.prediction_history if e['confidence'] <= 50),
                        '51-70%': sum(1 for e in st.session_state.prediction_history if 50 < e['confidence'] <= 70),
                        '71-85%': sum(1 for e in st.session_state.prediction_history if 70 < e['confidence'] <= 85),
                        '86-95%': sum(1 for e in st.session_state.prediction_history if 85 < e['confidence'] <= 95),
                        '96-100%': sum(1 for e in st.session_state.prediction_history if e['confidence'] > 95)
                    }
                    max_conf_count = max(confidence_ranges.values()) if confidence_ranges.values() else 1
                    
                    text_color = '#d1d5db' if st.session_state.dark_mode else '#4b5563'
                    bg_color = '#374151' if st.session_state.dark_mode else '#e5e7eb'
                    
                    for range_name, count in confidence_ranges.items():
                        width = (count / max_conf_count * 100) if max_conf_count > 0 else 0
                        range_html = f'''
                        <div style="margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span style="color: {text_color}; font-size: 0.9em;">{range_name}</span>
                                <span style="color: {text_color};">{count}</span>
                            </div>
                            <div style="background-color: {bg_color}; height: 20px; border-radius: 5px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #3b82f6, #60a5fa); height: 100%; width: {width}%; transition: width 0.3s;"></div>
                            </div>
                        </div>
                        '''
                        st.markdown(range_html, unsafe_allow_html=True)
                    st.caption("Distribution of confidence scores across predictions")
                
                st.divider()
                
                st.markdown("### Session Summary")
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.markdown("**Prediction Breakdown**")
                    st.write(f"• Total Predictions: **{total_predictions}**")
                    st.write(f"• Spam Detected: **{spam_count}** ({spam_percentage:.1f}%)")
                    st.write(f"• Not Spam: **{ham_count}** ({100-spam_percentage:.1f}%)")
                
                with summary_col2:
                    st.markdown("**Confidence Analysis**")
                    st.write(f"• Current Prediction: **{current_confidence}%**")
                    st.write(f"• Average Confidence: **{avg_confidence:.1f}%**")
                    high_confidence = sum(1 for e in st.session_state.prediction_history if e['confidence'] >= 90)
                    st.write(f"• High Confidence (≥90%): **{high_confidence}** predictions")
    else:
        st.warning("Please enter a message to classify.")

with st.sidebar:
    if not st.session_state.dark_mode:
        st.markdown('<h2 style="color: #1e40af; margin-bottom: 1rem;">Prediction History</h2>', unsafe_allow_html=True)
    else:
        st.header("Prediction History")
    
    if st.session_state.prediction_history:
        total_predictions = len(st.session_state.prediction_history)
        spam_count = sum(1 for entry in st.session_state.prediction_history if entry['result'] == 'Spam')
        ham_count = total_predictions - spam_count
        
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.dark_mode:
                st.markdown(f"""
                    <div style="padding: 1rem; background-color: #f9fafb; border-radius: 0.5rem;">
                        <div style="color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem;">Total</div>
                        <div style="color: #1f2937; font-size: 1.5rem; font-weight: 600;">{total_predictions}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("Total", total_predictions)
        with col2:
            if not st.session_state.dark_mode:
                st.markdown(f"""
                    <div style="padding: 1rem; background-color: #f9fafb; border-radius: 0.5rem;">
                        <div style="color: #dc2626; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.25rem;">Spam</div>
                        <div style="color: #1f2937; font-size: 1.5rem; font-weight: 600;">{spam_count}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("Spam", spam_count)
        
        st.divider()
        
        for idx, entry in enumerate(st.session_state.prediction_history):
            with st.container():
                if entry['result'] == 'Spam':
                    badge_color = "#dc2626"
                else:
                    badge_color = "#16a34a"
                
                message_preview = entry['message'][:50] + ('...' if len(entry['message']) > 50 else '')
                
                st.markdown(f"""
                    <div style="padding: 10px; margin-bottom: 10px; border-left: 3px solid {badge_color}; 
                                background-color: {'#1f2937' if st.session_state.dark_mode else '#f9fafb'}; 
                                border-radius: 5px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: {badge_color}; font-weight: 600;">{entry['result']}</span>
                            <span style="font-size: 0.8em; color: {'#9ca3af' if st.session_state.dark_mode else '#6b7280'};">
                                {entry['timestamp'].split()[1]}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.text(message_preview)
                
                st.markdown(f"""
                    <div style="font-size: 0.85em; color: {'#9ca3af' if st.session_state.dark_mode else '#6b7280'}; margin-top: -10px; margin-bottom: 10px;">
                        Confidence: {entry['confidence']}%
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Delete", key=f"delete_{entry['id']}", use_container_width=True):
                    st.session_state.prediction_history = [
                        e for e in st.session_state.prediction_history if e['id'] != entry['id']
                    ]
                    st.rerun()
                
                if idx < len(st.session_state.prediction_history) - 1:
                    st.divider()
        
        st.divider()
        if st.button("Clear All History", use_container_width=True, type="secondary"):
            st.session_state.prediction_history = []
            st.rerun()
    else:
        st.info("No predictions yet. Your prediction history will appear here.")
    
    if not st.session_state.dark_mode:
        st.markdown("""
            <style>
            div[data-testid="stToggle"] button[role="switch"],
            div[data-testid="stToggle"] button {
                background-color: #4b5563 !important;
                border-color: #4b5563 !important;
            }
            div[data-testid="stToggle"] button[aria-checked="true"] {
                background-color: #1f2937 !important;
                border-color: #1f2937 !important;
            }
            div[data-testid="stToggle"] button[aria-checked="false"] {
                background-color: #4b5563 !important;
                border-color: #4b5563 !important;
            }
            </style>
        """, unsafe_allow_html=True)
