import streamlit as st
import pandas as pd
import numpy as np
import pickle
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download necessary NLTK resources
nltk.download('stopwords')

# Load the trained model and CountVectorizer from pickle files
cv = pickle.load(open('cv-transform.pkl', 'rb'))
classifier = pickle.load(open('spam-sms-mnb-model.pkl', 'rb'))

# Initialize a PorterStemmer
ps = PorterStemmer()

# Function to clean the message before prediction
def clean_message(message):
    # Cleaning special character from the message
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=message)

    # Converting the entire message into lower case
    message = message.lower()

    # Tokenizing the review by words
    words = message.split()

    # Removing the stop words
    words = [word for word in words if word not in set(stopwords.words('english'))]

    # Stemming the words
    words = [ps.stem(word) for word in words]

    # Joining the stemmed words
    cleaned_message = ' '.join(words)
    
    return cleaned_message

# Streamlit app layout
st.title("SMS Spam Classifier")
st.markdown("This is a simple SMS spam classifier built using Naive Bayes and NLP.")

# Get user input (SMS message)
user_input = st.text_area("Enter your message:")

if st.button("Predict"):
    # Clean the user input message
    cleaned_input = clean_message(user_input)

    # Convert the cleaned input to a bag of words using the trained CountVectorizer
    input_vector = cv.transform([cleaned_input]).toarray()

    # Predict whether the message is spam or ham (not spam)
    prediction = classifier.predict(input_vector)
    
    if prediction == 1:
        st.write("Prediction: This is a **Spam** message.")
    else:
        st.write("Prediction: This is a **Ham** message (Not Spam).")

