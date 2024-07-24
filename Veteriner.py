import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g

# Veteriner ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - veterinarian_main_page
#   - veterinarian_info_page
#   - write_prescription_page
#   - past_patients_page
def veterinarian_main_page():
    st.title("Veteriner Ana Sayfa")
    st.write("Aktif Randevular")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Reçete Yaz"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Write Prescription"
            st.rerun()
    with col2:
        if st.button("Geçmiş Hastalar"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Past Patients"
            st.rerun()
    with col3:
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Info Page"
            st.rerun()

def veterinarian_info_page():
    st.title("Bilgilerim")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        tc_kimlik_no = st.number_input("TC Kimlik No", value=None, format="%.0f")
        if tc_kimlik_no and not g.is_valid_tc(tc_kimlik_no):
            st.error("TC kimlik numarası 11 haneli olmalıdır.")

    with col2:
        email_adresi = st.text_input("E-Mail Adresi")
        telefon = st.number_input("Telefon Numarası", value=None, format="%.0f", placeholder="5__")
        if telefon and not g.is_valid_tel(telefon):
            st.error("Geçersiz telefon numarası.")
        adres = st.text_input("Adres")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):
            if g.is_valid_tc(tc_kimlik_no) and g.is_valid_tel(telefon):
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database
            else:
                st.error("Lütfen bilgileri doğru formatta girin.")
    with col2:
        if st.button("Şifreyi Değiştir"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Change Password"
            st.rerun()

# Reçete yaz sayfası fonksiyonu
def write_prescription_page():
    st.title("Reçete Yaz")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    st.selectbox("Hastalar", options=["Hasta 1", "Hasta 2"])  # Placeholder options
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("İlaç")
    with col2:
        st.text_area("Doz")
    st.text_area("Açıklama")
    if st.button("Reçeteyi Onayla"):
        st.write("Reçete onaylandı!")  # Placeholder for prescription approval

# Geçmiş hastalar sayfası fonksiyonu
def past_patients_page():
    st.title("Geçmiş Hastalar")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    st.write("Geçmiş Hastalar Listesi (Hastayı seçer, geçmiş bilgiler görüntülenir)")