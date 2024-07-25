import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page

# Ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - main_page
#   - register_page

def main_page():
    st.title("Ana Sayfa")
    st.write("Bu, ana sayfanızdır.")
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://i.pinimg.com/564x/5e/16/49/5e1649c42a84d94f7a98535ec85f0ac6.jpg"  style="width: 350px;"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    mail = st.text_input("Mail Adresi", key="login_email")
    sifre = st.text_input("Şifre", type="password", key="login_password")
    rol = ""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Giriş"):
                query =  "SELECT * FROM bil372_project.kullanıcı where email = '{}' and şifre = '{}'".format(mail, sifre)
                data = get_data(query)

                if data is not None and not data.empty:
                    #st.session_state.kullanıcı_id = data.iloc[0]['KullanıcıID'] 
                    id = data.iloc[0]['KullanıcıID']
                    rol=st.session_state.rol = data.iloc[0]['Rol']

                    st.session_state.prev_page = st.session_state.page
                    if(rol=="kullanıcı"):
                        st.session_state.kullanıcı_id = data.iloc[0]['KullanıcıID']
                        st.session_state.page = "User Main"
                    elif(rol=="admin"):
                        st.session_state.admin_id = data.iloc[0]['KullanıcıID']
                        st.session_state.page = "Admin Main"
                    elif(rol=="veteriner"):
                        st.session_state.veteriner_id = data.iloc[0]['KullanıcıID']
                        st.session_state.page = "Veterinarian Main"
                    else:
                        st.error("Hatalı veritabanı verisi")
                    st.rerun()
                else:
                    st.write(data)
                    st.write(query)
                    st.write("Kullanıcı bulunamadı veya yanlış giriş bilgileri.")
        

    with col2:
        if st.button("Kayıt Ol"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Register"
            st.rerun()

# Kayıt ol sayfası fonksiyonu
# TODO bu kısmın sıralaması duzeni biraz degisebilir
def register_page():
    st.title("Kullanıcı Kayıt Ol")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    mail = st.text_input("Mail Adresi", key="register_email")
    sifre = st.text_input("Şifre", type="password", key="register_password")
    isim = st.text_input("İsim", key="register_name")
    soyisim = st.text_input("Soyisim", key="register_surname")
    il = st.text_input("İl", key="register_city")
    ilce = st.text_input("İlce", key="register_suborb")
    mahalle = st.text_input("Mahalle", key="register_neighboor")

    if st.button("Kayıt Ol"):
        id = get_highest_id('kullanıcı', 'KullanıcıID')
        id = id + 1        
        insert_query_kullanici = """
        INSERT INTO kullanıcı (kullanıcıID, email, şifre, rol)
        VALUES (%s, %s, %s, %s)
        """
        params = (id, mail, sifre, 'kullanıcı')

        insert_data(insert_query_kullanici, params)

        
        insert_query_hayvan_sahibi = """
        INSERT INTO hayvansahibi (kullanıcıID, isim, soyisim, il, ilçe,mahalle)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (id, isim, soyisim, il, ilce, mahalle)
        insert_data(insert_query_hayvan_sahibi, params)

        st.session_state.prev_page = st.session_state.page
        st.session_state.page = "Ana Sayfa"
        st.rerun()