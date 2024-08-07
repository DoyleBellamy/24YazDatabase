import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data


# İlaç ekle sayfası fonksiyonu
def add_medicine_page():
    st.title("İlaç Ekle")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    ilac_ad = st.text_input("İlaç Adı")
    ilac_toplam_ucret = st.number_input("Toplam Ücret", value=None, format="%.0f")
    ilac_miktar = st.number_input("Miktar", value=None, format="%.0f")

    if st.button("Ekle"):
        query =  "SELECT * FROM bil372_project.ilaçlar where isim = '{}' and adminId = '{}'".format(ilac_ad, str(st.session_state.admin_id))
        data = get_data(query)

        # Eger bu admin tarafından eklenen ilac zaten bulunuyorsa eski veriyi güncelliyoruz ekliyoruz
        if data is not None and not data.empty:
            # Veri mevcut, güncelle
            ilac_id = data.iloc[0]['İlaçID']
            # TODO kodu temizle
            eski_toplam_ucret = data.iloc[0]['Fiyat']
            eski_toplam_miktar = data.iloc[0]['Miktar']
            
            guncel_ucret = int(eski_toplam_ucret) + int(ilac_toplam_ucret)
            guncel_miktar = int(eski_toplam_miktar) + int(ilac_miktar)

            update_ilac = """
            UPDATE ilaçlar
            SET Fiyat = %s, Miktar = %s
            WHERE ilaçId = %s
            """
            update_params = (str(guncel_ucret), str(guncel_miktar), str(ilac_id))
            update_data(update_ilac, update_params)

        # Eger bu admin tarafından eklenen ilac zaten bulunmuyorsa yenisini ekliyoruz
        else:
            id = get_highest_id('ilaçlar', 'İlaçID') + 1
            insert_ilac_admin = """
            INSERT INTO ilaçlar (ilaçId, isim, Fiyat, Miktar, AdminId)
            VALUES (%s, %s, %s, %s, %s)
            """
            # Burada str()'ler gereksiz olabilir
            params = (str(id), ilac_ad, str(ilac_toplam_ucret), str(ilac_miktar), str(st.session_state.admin_id))

            insert_data(insert_ilac_admin, params)
        
        st.write("İlaç eklendi!")  # Placeholder for adding medicine to the database