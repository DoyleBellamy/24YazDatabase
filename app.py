import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
#from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import Admin, GeneralUser, Main, User, Veteriner

# st.session_state kullanarak kullanıcı_id tanımlama
if 'kullanıcı_id' not in st.session_state:
    st.session_state.kullanıcı_id = None

if 'rol' not in st.session_state:
    st.session_state.rol = None

if 'admin_id' not in st.session_state:
    st.session_state.admin_id = None

if 'veteriner_id' not in st.session_state:
    st.session_state.veteriner_id = None


# Başlangıçta session state'i ayarla
if 'page' not in st.session_state:
    st.session_state.page = "Ana Sayfa"
    st.session_state.prev_page = None

# Seçilen sayfayı göster
if st.session_state.page == "Ana Sayfa":
    Main.main_page()
elif st.session_state.page == "Register":
    Main.register_page()
elif st.session_state.page == "User Main":
    User.user_main_page()
elif st.session_state.page == "Past Appointments":
    User.past_appointments_page()
elif st.session_state.page == "User Info":
    User.user_info_page()
elif st.session_state.page == "Add Animal":
    User.add_animal_page()
elif st.session_state.page == "Book Appointment":
    User.book_appointment_page()
elif st.session_state.page == "Admin Main":
    Admin.admin_main_page()
elif st.session_state.page == "Add Veterinarian":
    Admin.add_veterinarian_page()
elif st.session_state.page == "Add Medicine":
    add_medicine_page()
elif st.session_state.page == "Admin Info":
    Admin.admin_info_page()
elif st.session_state.page == "Veterinarian Main":
    Veteriner.veterinarian_main_page()
elif st.session_state.page == "Write Prescription":
    Veteriner.write_prescription_page()
elif st.session_state.page == "Past Patients":
    Veteriner.past_patients_page()
elif st.session_state.page == "Veterinarian Add Times Avaliable":
    Admin.add_veterinarian_avaliable_time_page()
elif st.session_state.page == "Veterinarian Info":
    Veteriner.veterinarian_info_page()
elif st.session_state.page == "Change Password":
    GeneralUser.change_password_page()
