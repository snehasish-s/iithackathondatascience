import os
import pickle

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')


def train_and_save_model():
    """Train a simple Logistic Regression on Iris and save it to MODEL_PATH."""
    data = load_iris()
    X = data.data
    y = data.target

    clf = LogisticRegression(max_iter=200)
    clf.fit(X, y)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({'model': clf, 'target_names': data.target_names}, f)

    return clf, data.target_names


def load_model():
    """Load model from disk; train and save if not available or corrupted."""
    if not os.path.exists(MODEL_PATH):
        clf, names = train_and_save_model()
        return clf, names

    try:
        with open(MODEL_PATH, 'rb') as f:
            data = pickle.load(f)
            model = data.get('model')
            names = data.get('target_names')
            if model is None:
                raise ValueError('No model in pickle')
            return model, names
    except Exception:
        # If loading failed, retrain
        clf, names = train_and_save_model()
        return clf, names


def predict(features):
    """Predict class and probability for given feature vector (iterable)."""
    model, names = load_model()
    arr = np.array(features, dtype=float).reshape(1, -1)
    proba = model.predict_proba(arr)[0]
    pred = int(model.predict(arr)[0])
    return {
        'class_index': pred,
        'class_name': str(names[pred]),
        'probability': float(proba[pred]),
        'all_probabilities': [float(x) for x in proba]
    }
