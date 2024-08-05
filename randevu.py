import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g
import datetime as d

def randevu(start,end):

    weekdays = {
        0 : "Pazartesi",
        1 : "Salı",
        2 : "Çarşamba",
        3 : "Perşembe",
        4 : "Cuma",
        5 : "Cumartesi",
        6 : "Pazar"
    }

    print("randevu alma işlemi başlıyor")
    print(st.session_state.veteriner_id)
    print(st.session_state.kullanıcı_id)
    #Burada where kısmına end ve start arasındaki tüm randevuları getirtebiliriz
    vet_randevular ="""
    SELECT * FROM randevu WHERE VeterinerID = '{}' 
    """.format(st.session_state.veteriner_id)
    randevular = get_data(vet_randevular)
    print(randevular)
    # Uygun zamanları getir 
    vet_uygun_q = """
    SELECT 
    u.SaatID, 
    u.VeterinerID,
    s.Gün, 
    STR_TO_DATE(CONCAT('2024-01-01 ', 
        LPAD(s.Saat, 2, '0'),
        ':',
        LPAD(s.Dakika, 2, '0'),
        ':00'
    ),'%Y-%m-%d %H:%i:%s')
     AS Tarih
    FROM 
    uygundur u
    JOIN 
    saatler s ON u.SaatID = s.SaatID
    WHERE u.VeterinerID = '{}' AND s.Gün = '{}'
    """.format(st.session_state.veteriner_id,"Pazartesi")
    uygun = get_data(vet_uygun_q)
    print(uygun)

    randevu_olustur = """
            INSERT INTO randevu (VeterinerID, SahipID, Tarih)
            VALUES (%s,%s, %s)
        """
    
    #print(start.strftime('%Y-%m-%d %H:%M:%S'))
    print(weekdays[start.weekday()])

    i=0
    date = start
    while date <= end :
        print(date)
        date += d.timedelta(days=1)
        i += 1
    
    print(start.strftime('%Y-%m-%d'))
    #print(f"Saat: {start.strftime('%Y-%m-%d').hour}:{start.strftime('%Y-%m-%d').minute}")
    params = str(st.session_state.veteriner_id), str(st.session_state.kullanıcı_id), start.strftime('%Y-%m-%d')
    insert_data(randevu_olustur,params)