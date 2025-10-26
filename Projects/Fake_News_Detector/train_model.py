import pickle
import os
from scripts.prepare_dataset import (
    X_train_tfidf, X_test_tfidf, y_train, y_test,
    model, tfidf, accuracy, precision, recall, f1
)

# Save metrics
os.makedirs('models', exist_ok=True)
metrics_text = f"""
=== FAKE NEWS DETECTOR - MODEL METRICS ===

Model: Logistic Regression
Vectorizer: TF-IDF (max_features=5000, ngram_range=(1,2))

PERFORMANCE METRICS:
- Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)
- Precision: {precision:.4f} ({precision*100:.2f}%)
- Recall:    {recall:.4f} ({recall*100:.2f}%)
- F1-Score:  {f1:.4f}

INTERPRETATION:
- Accuracy: Percentage of correct predictions
- Precision: Of predicted fake news, how many were actually fake
- Recall: Of actual fake news, how many were detected
- F1-Score: Harmonic mean of precision and recall

DATASET:
- Training samples: {len(X_train_tfidf)}
- Test samples: {len(X_test_tfidf)}
- Total features: {X_train_tfidf.shape[1]}
"""

with open('models/metrics.txt', 'w') as f:
    f.write(metrics_text)

print(metrics_text)
print("✓ Metrics saved to models/metrics.txt")
