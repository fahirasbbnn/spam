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

# Mengunduh resource yang dibutuhkan dari NLTK
nltk.download('stopwords')

# Memuat model yang sudah dilatih dan CountVectorizer dari file pickle
cv = pickle.load(open('cv-transform.pkl', 'rb'))
classifier = pickle.load(open('spam-sms-mnb-model.pkl', 'rb'))

# Inisialisasi PorterStemmer
ps = PorterStemmer()

# Fungsi untuk membersihkan pesan sebelum diprediksi
def clean_message(message):
    # Menghapus karakter khusus dari pesan
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=message)

    # Mengubah seluruh pesan menjadi huruf kecil
    message = message.lower()

    # Tokenisasi pesan berdasarkan kata
    words = message.split()

    # Menghapus stop words
    words = [word for word in words if word not in set(stopwords.words('english'))]

    # Melakukan stemming pada kata-kata
    words = [ps.stem(word) for word in words]

    # Menggabungkan kata-kata yang sudah di-stem
    cleaned_message = ' '.join(words)
    
    return cleaned_message

# Layout aplikasi Streamlit
st.title("Klasifikasi SMS Spam")
st.markdown("Ini adalah aplikasi sederhana untuk mengklasifikasikan SMS sebagai spam atau tidak menggunakan Naive Bayes dan NLP.")

# Mendapatkan input dari pengguna (pesan SMS)
user_input = st.text_area("Masukkan pesan Anda:")

if st.button("Prediksi"):
    # Membersihkan input pesan dari pengguna
    cleaned_input = clean_message(user_input)

    # Mengubah input yang sudah dibersihkan menjadi bag of words menggunakan CountVectorizer yang telah dilatih
    input_vector = cv.transform([cleaned_input]).toarray()

    # Memprediksi apakah pesan tersebut spam atau bukan (ham)
    prediction = classifier.predict(input_vector)
    
    if prediction == 1:
        st.write("Prediksi: Ini adalah pesan **Spam**.")
    else:
        st.write("Prediksi: Ini adalah pesan **Ham** (Bukan Spam).")
