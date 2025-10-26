import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import os

# Create sample dataset (in production, use real fake news dataset)
# You can download from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
np.random.seed(42)

# Sample data for demonstration
real_headlines = [
    "Scientists discover new species in Amazon rainforest",
    "Global temperatures rise by 1.5 degrees this year",
    "New vaccine shows 95% effectiveness in trials",
    "Stock market reaches all-time high",
    "Researchers develop breakthrough cancer treatment",
    "International climate agreement signed by 195 nations",
    "Tech company announces new AI research division",
    "University study reveals benefits of exercise",
    "Government approves new infrastructure bill",
    "Medical breakthrough in Alzheimer's research"
]

fake_headlines = [
    "Celebrities secretly control world governments",
    "Miracle cure discovered but hidden by big pharma",
    "5G towers cause COVID-19 spread",
    "Moon landing was completely faked",
    "Aliens spotted landing in major city",
    "Secret government experiment exposed",
    "Billionaire plans to destroy economy",
    "Shocking truth about water revealed",
    "Conspiracy: Birds are government drones",
    "Celebrity dies in secret accident"
]

# Create DataFrame
data = pd.DataFrame({
    'text': real_headlines + fake_headlines,
    'label': [1] * len(real_headlines) + [0] * len(fake_headlines)
})

print(f"Dataset shape: {data.shape}")
print(f"Real news: {(data['label'] == 1).sum()}")
print(f"Fake news: {(data['label'] == 0).sum()}")

# Clean text
data['text'] = data['text'].str.lower().str.strip()

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    data['text'], data['label'], test_size=0.2, random_state=42, stratify=data['label']
)

print(f"\nTraining set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print(f"TF-IDF features: {X_train_tfidf.shape[1]}")

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_tfidf, y_train)

# Evaluate
y_pred = model.predict(X_test_tfidf)
y_pred_proba = model.predict_proba(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"\n=== Model Performance ===")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

# Save model and vectorizer
os.makedirs('models', exist_ok=True)
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

print("\n✓ Model and vectorizer saved successfully!")
