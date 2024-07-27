import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g

def randevu(start,end):
    print("randevu alma işlemi başlıyor")
    print(st.session_state.veteriner_id)
    print(st.session_state.kullanıcı_id)
    q = """
            INSERT INTO randevu (VeterinerID, SahipID, Tarih)
            VALUES (%s,%s, %s)
        """
    #print(start.strftime('%Y-%m-%d %H:%M:%S'))
    params = str(st.session_state.veteriner_id), str(st.session_state.kullanıcı_id), start.strftime('%Y-%m-%d')
    insert_data(q,params)