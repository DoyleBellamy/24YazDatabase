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
    return not bool(re.search('[A-Z]|[a-z]|[öÖİŞşĞğçÇIıüÜ]', input_value)) and len(input_value) == 11

def is_valid_tel(input_value):
    return not bool(re.search('[A-Z]|[a-z]|[öÖİŞşĞğçÇIıüÜ]', input_value)) and len(input_value) == 10

# Şifre değiştirme sayfası
# Diğer roller tarafından da kullanılabilecek bir fonksiyon olduğu için general user dosyasına alındı
# Kullanılacak sayfalarda import edilmesi gerekiyor
def change_password_page(user_id):
    st.title("Şifre Değiştir")
    current_password = st.text_input("Mevcut Şifre", type="password")
    new_password = st.text_input("Yeni Şifre", type="password")
    confirm_password = st.text_input("Yeni Şifreyi Onayla", type="password")

    if st.button("Şifreyi Değiştir"):
        # Boşluk kontrolü
        if ((current_password is not None and current_password!="")and (new_password is not None  and new_password!="")and (confirm_password is not None and confirm_password!="")):
            if new_password != confirm_password:
                st.error("Yeni şifreler uyuşmuyor.")
            else:
                if user_id is None:
                    st.error("Kullanıcı kimliği bulunamadı.")
                else:
                    user_id = int(user_id)  # Ensure user_id is an integer
                    query = "SELECT Şifre FROM bil372_project.kullanıcı WHERE KullanıcıID = '{}'".format(user_id)
                    data = get_data(query)
                    print("Select Query Data:", data)
                
                    if data is not None and not data.empty and data.iloc[0]['Şifre'] == current_password:
                        update_query = "UPDATE bil372_project.kullanıcı SET Şifre = %s WHERE KullanıcıID = %s"
                        params = new_password, user_id
                        print("Update Query:", update_query)
                        #update_data(update_query, (new_password, user_id))
                        update_data(update_query, params)
                        st.write("Şifre Değiştirildi.")
                    else:
                        st.error("Mevcut şifre yanlış.")
        else:
            st.error("Boş bırakılamaz.")
