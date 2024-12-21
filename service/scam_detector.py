import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved vectorizer
with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Load the pickle file
with open('model.pkl', 'rb') as file:
    loaded_data = pickle.load(file)