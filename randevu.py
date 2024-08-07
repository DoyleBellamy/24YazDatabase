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

    vet_uygun_q ="""
    with
    saat as(
    SELECT 
        u.SaatID, 
        u.VeterinerID,
        s.Gün, 
        STR_TO_DATE(CONCAT('{}', 
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
        WHERE u.VeterinerID = '{}' AND s.Gün = '{}'),
    ran as (
    SELECT * FROM randevu as r
    WHERE r.tarih >='{}'
    AND r.tarih <'{}')
    Select s.VeterinerID, s.Gün, s.Tarih
    from saat as s
    left join ran as r
    on s.Tarih = r.Tarih
    where r.Tarih is null
    order by r.Tarih asc
    ;
    """

    randevu_olustur = """
            INSERT INTO randevu (VeterinerID, SahipID, Tarih)
            VALUES (%s,%s, %s)
        """

    i=0
    date = start
    success = False
    while date <= end :
        q = vet_uygun_q.format(date,st.session_state.veteriner_id,weekdays[date.weekday()],date,date + d.timedelta(days=1))
        uygun = get_data(q)

        if uygun is not None and not uygun.empty:

            try:
                params = str(st.session_state.veteriner_id), str(st.session_state.kullanıcı_id), str(uygun.iloc[0]['Tarih'])
                insert_data(randevu_olustur,params)
                success = True
                st.success("Randevunuz başarıyla oluşturulmuştur.")
            except:
                success = True
                st.error("Randevu oluşturulurken bir hata oluştu. Lütfen tekrar deneyeniz")
            break
        date += d.timedelta(days=1)
        i += 1
    if not success:
        st.error("Seçtiğiniz aralıkta uygun randevu bulunamadı. Farklı tarihlerle tekrar deneyiniz.")
    
    