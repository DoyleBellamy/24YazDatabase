import streamlit as st
import mysql.connector
import pandas as pd

# MySQL veritabanına bağlanmak için gereken bilgiler
db_config = {
    'user': 'root',
    'password': 'umut',
    'host': '127.0.0.1',
    'database': 'bil372_project',
}

# MySQL bağlantısı oluştur
def create_connection():
    return mysql.connector.connect(**db_config)

# MySQL veritabanından veri almak için fonksiyon
def get_data(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Ana sayfa fonksiyonu
def main_page():
    st.title("Ana Sayfa")
    st.write("Bu, ana sayfanızdır.")
    if st.button("Sayfa 1'e Git"):
        st.session_state.page = "Sayfa 1"
        st.experimental_rerun()

# Sayfa 1 fonksiyonu
def page1():
    st.title("Sayfa 1")
    st.write("Bu, Sayfa 1'dir.")
    st.image("C:\\Users\\umutozdemir\\Desktop\\GKEV9LXW8AAO1Eq.jpg", caption="Örnek Resim")
    query = st.text_input("SQL Sorgunuzu Girin:", "SELECT * FROM your_table")
    if st.button("Verileri Getir"):
        data = get_data(query)
        st.write(data)
    if st.button("Sayfa 2'ye Git"):
        st.session_state.page = "Sayfa 2"
        st.experimental_rerun()

# Sayfa 2 fonksiyonu
def page2():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: black;
        }
        div.stButton > button {
            background-color: grey;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Sayfa 2")
    st.write("Bu, Sayfa 2'dir.")
    if st.button("Ana Sayfa'ya Git"):
        st.session_state.page = "Ana Sayfa"
        st.experimental_rerun()

# Başlangıçta session state'i ayarla
if 'page' not in st.session_state:
    st.session_state.page = "Ana Sayfa"

# Seçilen sayfayı göster
if st.session_state.page == "Ana Sayfa":
    main_page()
elif st.session_state.page == "Sayfa 1":
    page1()
elif st.session_state.page == "Sayfa 2":
    page2()



