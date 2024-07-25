import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
# Yardımcı fonksiyonlar utile de taşınabilir ama şimdilik buraya alıyorum
# Belli bir role kısıtlı olmayan ve tekrar kullanılan sayfalar ve yardımcı fonksiyonlar burada saklanır
# İçindeki sayfalar:
#   - change_password_page

# Yardımcı fonksiyonlar
def is_valid_tc(input_value):
    #İnteger olarak alınca hata veriyor
    #input_value = int(input_value)
    #return len(str(input_value)) == 11
    return not bool(re.search('[A-Z]|[a-z]|[öÖİŞşĞğçÇIıüÜ]', input_value)) and len(input_value) == 11

def is_valid_tel(input_value):
    #input_value = int(input_value)
    return not bool(re.search('[A-Z]|[a-z]|[öÖİŞşĞğçÇIıüÜ]', input_value)) and len(input_value) == 11

# TODO DEĞİŞTİRDİ OLARAK GÖSTERİYOR TÜM IFLERI GEÇİYOR ANCAK get_data ÇAĞRILDIĞINDA ESKİ ŞİFRE GÖZÜKÜYOR
# Şifre değiştirme sayfası
def change_password_page():
    st.title("Şifre Değiştir")
    current_password = st.text_input("Mevcut Şifre", type="password")
    new_password = st.text_input("Yeni Şifre", type="password")
    confirm_password = st.text_input("Yeni Şifreyi Onayla", type="password")

    if st.button("Şifreyi Değiştir"):
        if new_password != confirm_password:
            st.error("Yeni şifreler uyuşmuyor.")
        else:
            user_id = (st.session_state.kullanıcı_id or 
                       st.session_state.admin_id or 
                       st.session_state.veteriner_id)
            if user_id is None:
                st.error("Kullanıcı kimliği bulunamadı.")
            else:
                user_id = int(user_id)  # Ensure user_id is an integer
                query = "SELECT şifre FROM bil372_project.kullanıcı WHERE KullanıcıID = '{}'".format(user_id)
                data = get_data(query)
                print("Select Query Data:", data)
                
                if data is not None and not data.empty and data.iloc[0]['şifre'] == current_password:
                    update_query = "UPDATE bil372_project.kullanıcı SET şifre = '{}' WHERE KullanıcıID = '{}'".format(new_password, user_id)
                    print("Update Query:", update_query)
                    update_data(update_query, (new_password, user_id))
                    st.write("Şifre Değiştirildi.")
                else:
                    st.error("Mevcut şifre yanlış.")