import streamlit as st
import pickle
import pandas as pd
import numpy as np
from io import StringIO
import os

# Set page config
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .real-news {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .fake-news {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Load model and vectorizer
@st.cache_resource
def load_model():
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/tfidf.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    return model, tfidf

try:
    model, tfidf = load_model()
except FileNotFoundError:
    st.error("❌ Model files not found. Please run the training script first.")
    st.stop()

# Title
st.title("📰 Fake News Detector")
st.markdown("Detect whether a news headline is real or fake using Machine Learning")

# Tabs
tab1, tab2, tab3 = st.tabs(["Single Prediction", "Batch Upload", "About"])

# ============ TAB 1: Single Prediction ============
with tab1:
    st.header("Check a Single Headline")
    
    headline = st.text_area(
        "Enter a news headline:",
        placeholder="Type or paste a headline here...",
        height=100
    )
    
    if st.button("🔍 Analyze Headline", use_container_width=True):
        if headline.strip():
            # Preprocess
            headline_clean = headline.lower().strip()
            
            # Vectorize
            headline_tfidf = tfidf.transform([headline_clean])
            
            # Predict
            prediction = model.predict(headline_tfidf)[0]
            confidence = model.predict_proba(headline_tfidf)[0]
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                if prediction == 1:
                    st.markdown(
                        f"""
                        <div class="real-news">
                        <h3>✅ REAL NEWS</h3>
                        <p>This headline appears to be <strong>genuine</strong>.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="fake-news">
                        <h3>⚠️ FAKE NEWS</h3>
                        <p>This headline appears to be <strong>suspicious</strong>.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with col2:
                st.metric("Confidence", f"{max(confidence) * 100:.2f}%")
            
            # Detailed breakdown
            st.subheader("Confidence Breakdown")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Real News Probability", f"{confidence[1] * 100:.2f}%")
            with col2:
                st.metric("Fake News Probability", f"{confidence[0] * 100:.2f}%")
            
            # Confidence chart
            chart_data = pd.DataFrame({
                'Category': ['Real News', 'Fake News'],
                'Confidence': [confidence[1] * 100, confidence[0] * 100]
            })
            st.bar_chart(chart_data.set_index('Category'))
        else:
            st.warning("Please enter a headline to analyze.")

# ============ TAB 2: Batch Upload ============
with tab2:
    st.header("Batch Check - Upload CSV")
    
    uploaded_file = st.file_uploader(
        "Upload a CSV file with headlines",
        type=['csv'],
        help="CSV should have a 'headline' or 'text' column"
    )
    
    if uploaded_file is not None:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Find text column
        text_column = None
        for col in ['headline', 'text', 'title', 'news']:
            if col in df.columns:
                text_column = col
                break
        
        if text_column is None:
            st.error(f"❌ CSV must contain one of these columns: headline, text, title, or news")
            st.write("Available columns:", df.columns.tolist())
        else:
            st.success(f"✓ Found '{text_column}' column with {len(df)} headlines")
            
            if st.button("🔍 Analyze All Headlines", use_container_width=True):
                # Process all headlines
                progress_bar = st.progress(0)
                predictions = []
                confidences = []
                
                for idx, headline in enumerate(df[text_column]):
                    headline_clean = str(headline).lower().strip()
                    headline_tfidf = tfidf.transform([headline_clean])
                    pred = model.predict(headline_tfidf)[0]
                    conf = model.predict_proba(headline_tfidf)[0]
                    
                    predictions.append("Real" if pred == 1 else "Fake")
                    confidences.append(max(conf))
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                # Add results to dataframe
                results_df = df.copy()
                results_df['Prediction'] = predictions
                results_df['Confidence'] = (confidences * 100).round(2)
                
                # Display results
                st.subheader("Results")
                st.dataframe(results_df, use_container_width=True)
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Headlines", len(results_df))
                with col2:
                    real_count = (results_df['Prediction'] == 'Real').sum()
                    st.metric("Real News", real_count)
                with col3:
                    fake_count = (results_df['Prediction'] == 'Fake').sum()
                    st.metric("Fake News", fake_count)
                with col4:
                    avg_conf = results_df['Confidence'].mean()
                    st.metric("Avg Confidence", f"{avg_conf:.2f}%")
                
                # Download results
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="fake_news_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# ============ TAB 3: About ============
with tab3:
    st.header("About This Project")
    
    st.markdown("""
    ### How It Works
    
    This Fake News Detector uses **Machine Learning** to classify news headlines as real or fake.
    
    **Technology Stack:**
    - **TF-IDF Vectorization**: Converts text into numerical features
    - **Logistic Regression**: Trained classification model
    - **Streamlit**: Interactive web interface
    
    ### Model Performance
    
    The model was trained on a dataset of real and fake news headlines and evaluated on test data.
    """)
    
    # Load and display metrics if available
    if os.path.exists('models/metrics.txt'):
        with open('models/metrics.txt', 'r') as f:
            metrics = f.read()
        st.code(metrics, language='text')
    else:
        st.info("Run the training script to generate performance metrics.")
    
    st.markdown("""
    ### Limitations
    
    - Model accuracy depends on training data quality
    - Headlines with ambiguous language may be misclassified
    - Real-time news trends may affect predictions
    - This is a demonstration model; use with caution
    
    ### How to Use
    
    1. **Single Prediction**: Enter a headline to get instant classification
    2. **Batch Upload**: Upload a CSV file with multiple headlines for analysis
    3. **Download Results**: Export predictions for further analysis
    """)
