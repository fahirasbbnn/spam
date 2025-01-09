import streamlit as st
import pandas as pd

# Memuat dataset yang sudah dibersihkan
df = pd.read_csv('Supermarket Sales Cleaned.csv')

# Membersihkan nama kolom untuk menghindari masalah dengan spasi yang tidak terlihat
df.columns = df.columns.str.strip()

# Periksa nama-nama kolom yang ada dalam dataset
st.write(df.columns)  # Menampilkan nama kolom

# Jika kolom 'Product line' tidak ada, tampilkan pesan kesalahan
if 'Product line' not in df.columns:
    st.error("Kolom 'Product line' tidak ditemukan dalam dataset!")
else:
    # Fungsi untuk mengklasifikasikan product line berdasarkan nama produk
    def classify_product_line(product_name):
        product_line = df[df['Product'].str.contains(product_name, case=False, na=False)]['Product line'].unique()
        return product_line

    # Fungsi untuk menghitung jumlah pembelian berdasarkan product line dan kota
    def count_purchases_by_product_line_and_city(product_line, city):
        count = df[(df['Product line'] == product_line) & (df['City'] == city)].shape[0]
        return count

    # Fungsi untuk mendapatkan rating berdasarkan product line dan kota
    def get_ratings_by_product_line_and_city(product_line, city):
        ratings = df[(df['Product line'] == product_line) & (df['City'] == city)]['Rating']
        return ratings

    # Fungsi untuk mendapatkan metode pembayaran berdasarkan product line dan kota
    def get_payments_by_product_line_and_city(product_line, city):
        payments = df[(df['Product line'] == product_line) & (df['City'] == city)]['Payment'].value_counts()
        return payments

    # Fungsi untuk mendapatkan detail product line tertentu
    def get_product_line_details(product_line):
        total_purchases = df[df['Product line'] == product_line].shape[0]
        payment_methods = df[df['Product line'] == product_line]['Payment'].value_counts()
        cities = df[df['Product line'] == product_line]['City'].value_counts()
        ratings = df[df['Product line'] == product_line]['Rating'].describe()
        return total_purchases, payment_methods, cities, ratings

    # Antarmuka Streamlit
    st.title('Aplikasi Klasifikasi Product Line dan Analisis Pembelian')

    product_name = st.text_input('Masukkan nama produk:')
    city = st.selectbox('Pilih kota:', df['City'].unique())
    product_line = st.selectbox('Pilih product line:', df['Product line'].unique())

    if product_name:
        classified_product_line = classify_product_line(product_name)
        if classified_product_line.size > 0:
            st.write(f'Product line untuk "{product_name}" adalah: {classified_product_line[0]}')
            
            purchase_count = count_purchases_by_product_line_and_city(classified_product_line[0], city)
            st.write(f'Jumlah pembelian untuk product line "{classified_product_line[0]}" di {city} adalah: {purchase_count}')
            
            ratings = get_ratings_by_product_line_and_city(classified_product_line[0], city)
            st.write(f'Rating untuk product line "{classified_product_line[0]}" di {city}:')
            st.write(ratings.describe())
            
            payments = get_payments_by_product_line_and_city(classified_product_line[0], city)
            st.write(f'Metode pembayaran untuk product line "{classified_product_line[0]}" di {city}:')
            st.write(payments)
        else:
            st.write(f'Tidak ditemukan product line untuk "{product_name}"')

    if product_line:
        total_purchases, payment_methods, cities, ratings = get_product_line_details(product_line)
        st.write(f'Total pembelian untuk product line "{product_line}": {total_purchases}')
        st.write(f'Metode pembayaran untuk product line "{product_line}":')
        st.write(payment_methods)
        st.write(f'Kota dengan pembelian terbanyak untuk product line "{product_line}":')
        st.write(cities)
        st.write(f'Rating untuk product line "{product_line}":')
        st.write(ratings)
