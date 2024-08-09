import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime
from datetime import timedelta  # timedelta fonksiyonunu import edin

# Veteriner ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - veterinarian_main_page
#   - veterinarian_info_page
#   - write_prescription_page
def veterinarian_main_page():
    st.title("Veteriner Ana Sayfa")
    st.write("Aktif Randevular")

    # TODO Buraya query'e aktifleri alacak şekilde bir where yazılmalı
    # Tüm randevular tarafında bunu farklı yazıcaz 
    # Fikir olarak bugünden 10 gün öncesi mesela aktiftir deyip daha da önceki olanlar için randevu falan eklenemez diyebiliriz
    get_query_veteriner_randevular = """
    SELECT * FROM bil372_project.randevu r
    Join hayvansahibi hs on hs.kullanıcıID = r.sahipID
    Join hastahayvan hh on hh.sahipID = hs.kullanıcıID
    WHERE veterinerID = %s and r.Tarih >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);
    """
    params = (str(st.session_state.veteriner_id),)
    
    selected_rows = pd.DataFrame()

    data = get_data(get_query_veteriner_randevular, params)
    if data is not None and not data.empty:
        # Convert data to a DataFrame
        df1 = pd.DataFrame(data)
        # Remove columns containing 'ID'
        df = df1.loc[:, ~df1.columns.str.contains('ID')].copy()
        if 'HastaID' in df1.columns:
            df.loc[:, 'HastaID'] = df1['HastaID']
        else:
            print("HastaID column does not exist in df1.")

        columns = df.columns.tolist()
        for i, col in enumerate(columns):
            if col == "İsim":
                columns[i] = "Sahip İsmi"
                break
        df.columns = columns

        # Create a GridOptionsBuilder instance
        gb = GridOptionsBuilder.from_dataframe(df)
        # Configure selection and layout options
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
        
        gb.configure_column("Tarih", filter="agDateColumnFilter")
        gridOptions = gb.build()

        # Display the grid with selectable rows
        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode='MODEL_CHANGED',
            enable_enterprise_modules=True, 
            width='100%',
            height=200
        )
        selected_rows = grid_response['selected_rows']

    else:
        st.warning("Randevu Bulunamadı.")

    # Burada hizalamalar yapılabilir
    col1, col2, col3 = st.columns(3)
    with col1:
        if selected_rows is not None and not selected_rows.empty:
            if st.button("Reçete Yaz"):
                st.session_state.prev_page = st.session_state.page
                st.session_state.hastaHayvan = selected_rows['HastaID'].iloc[0]
                st.session_state.page = "Write Prescription"
                st.rerun()
    with col2:
        # TODO Burada ismi değişen buton olacak. Aktif'ken sadece aktifler görünecek. Bir daha basınca tümü görünecek. 
        # Aktiften kasıt randevu tarihinin bugünden sonra olması diyebiliriz direkt
        if st.button("Tüm Randevular/Hastalar"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "All_Appointments"
            st.rerun()

    with col3:
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Veterinarian Info"
            st.rerun()

def veterinarian_info_page():

    # Veteriner bilgilerini getir

    # TODO Bu kodu düzeltmek gerek
    veteriner_info_query ="""
    SELECT * FROM veteriner INNER JOIN kullanıcı on kullanıcı.KullanıcıID = veteriner.KullanıcıID WHERE veteriner.KullanıcıID = '{}'
    """.format(st.session_state.veteriner_id)
    vet_info = get_data(veteriner_info_query)
    
    # Queryden gelen datadan ilgili bilgileri çek
    email_adresi = vet_info.iloc[0]['Email']
    isim = vet_info.iloc[0]['İsim']
    soyisim = vet_info.iloc[0]['Soyisim']
    tc_kimlik_no = vet_info.iloc[0]['TCNO']
    # Backendden 11 haneli telefon numarası geliyor fakat biz 10 haneli telefon numarası kontrolu yapıyoruz
    # bundan dolayı telefonun ilk hanesi olan 0 çıkarılarak telefona atanıyor.
    tel = vet_info.iloc[0]['TelefonNo']
    telefon = tel[1:len(tel)]
    ilce =vet_info.iloc[0]['İlçe']
    mah = vet_info.iloc[0]['Mahalle']
    il = vet_info.iloc[0]['İl']
    oda = vet_info.iloc[0]['OdaNO']

    st.title("Bilgilerim")
    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("İsim", value = isim)
        soyisim = st.text_input("Soyisim", value = soyisim)
        # TC kimlik numarasını görebilsin fakat değiştiremesin
        tc_kimlik_no = st.text_input("TC Kimlik No", value = tc_kimlik_no, disabled = True)    
        if tc_kimlik_no and not g.is_valid_tc(tc_kimlik_no):
            st.error("TC kimlik numarası 11 haneli olmalıdır.")
        il = st.text_input("İl", value = il)
        mah = st.text_input("Mahalle", value = mah)
        

    with col2:
        email_adresi = st.text_input("E-Mail Adresi", value = email_adresi)
        telefon = st.text_input("Telefon Numarası", placeholder="5__",value = telefon)
        if telefon and not g.is_valid_tel(telefon):
            st.error("Geçersiz telefon numarası.")
        oda = st.text_input("Oda Numarası", value = oda, disabled = True)
        ilce = st.text_input("İlce", value = ilce)
        

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):
            v_id = st.session_state.veteriner_id

            update_kul_query = """
            UPDATE kullanıcı SET Email = %s WHERE KullanıcıID = %s
            """
            params1 = email_adresi, int( v_id)

            update_sahip_query = """
            UPDATE veteriner SET İsim = %s, Soyisim = %s, TelefonNo = %s, İl = %s, İlçe = %s, Mahalle = %s WHERE KullanıcıID = %s
            """ 

            params2 = isim, soyisim,("0"+telefon), il, ilce, mah,int( v_id)

            print("Here we go!")
            try:
               # TODO Buradaki data1 ve data2 ise yaramiyorsa atanmasin
               data1 = update_data(update_kul_query,params1)
            except:
                st.error("Email adresiniz değiştirilirken bir hata oluştu.")
            try:
                data2 = update_data(update_sahip_query,params2)
            except:
                st.error("Hesap bilgileriniz değiştirilirken bir hata oluştu")
            else:
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database

    with col2:
        if st.button("Şifreyi Değiştir"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Veterinarian Change Password"
            st.rerun()
    # TODO Buna basinca geri sayfada biraz bozuluyor düzeltilebilir.   
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()


def veterinarian_change_password_page():
    g.change_password_page(st.session_state.veteriner_id)
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.session_state.prev_page = "Veterinarian Main"
        st.rerun()


# TODO Negatif doz verememesi hem SQL'de hem de burada eklenebilir
# TODO Buraya zaman kalırsa bir transaction eklenebilir
def write_prescription_page():
    st.title("Reçete Yaz")

    # Fetch the list of available ilaçlar from the database
    ilac_query = "SELECT İlaçID, İsim FROM ilaçlar"
    ilac_data = get_data(ilac_query)

    # Extracting the 'İsim' and 'İlaçID' into lists
    ilac_names = []
    ilac_ids = {}
    if ilac_data is not None and not ilac_data.empty:
        df_ilac = pd.DataFrame(ilac_data)
        ilac_names = df_ilac['İsim'].tolist()
        ilac_ids = {row['İsim']: row['İlaçID'] for _, row in df_ilac.iterrows()}

    # Eğer session_state içinde prescriptions yoksa, başlat
    if 'prescriptions' not in st.session_state:
        st.session_state.prescriptions = [{'ilac': ilac_names[0] if ilac_names else '', 'doz': 0}]

    # İlaç ve doz alanlarını dinamik olarak ekle
    for i, prescription in enumerate(st.session_state.prescriptions):
        col1, col2 = st.columns(2)
        with col1:
            selected_ilac = st.selectbox(
                f"İlaç {i+1}", 
                options=ilac_names,
                index=ilac_names.index(prescription['ilac']) if prescription['ilac'] in ilac_names else 0,
                key=f'ilac_{i}'
            )
            st.session_state.prescriptions[i]['ilac'] = selected_ilac
        with col2:
            # Dozu text_input ile al, sadece sayısal değerleri kabul et
            selected_doz = st.text_input(
                f"Doz (mg) {i+1}",
                value=prescription['doz'],
                key=f'doz_{i}'
            )
            # Girişin sadece sayı olduğundan emin ol
            if selected_doz.isdigit():
                st.session_state.prescriptions[i]['doz'] = int(selected_doz)
            else:
                st.session_state.prescriptions[i]['doz'] = 0
                st.warning(f"Lütfen geçerli bir doz girin (sadece sayılar).")

    # İlaç sayısını artır ve azalt butonları
    cola, colb = st.columns(2)
    with cola:
        if st.button("İlaç Ekle"):
            st.session_state.prescriptions.append({'ilac': ilac_names[0] if ilac_names else '', 'doz': 0})
    with colb:
        if st.button("İlaç Sil"):
            if len(st.session_state.prescriptions) > 1:
                st.session_state.prescriptions.pop()

    aciklama = st.text_area("Açıklama")

    if st.button("Reçeteyi Onayla"):
        # İlaç ve doz bilgilerini bastır
        empty_fields = False
        for prescription in st.session_state.prescriptions:
            if not prescription['ilac'] or not prescription['doz']:
                empty_fields = True
                break
        if not aciklama or aciklama.strip() == '':
            empty_fields = True
        
        if empty_fields:
            st.error("Lütfen tüm ilaç, doz ve açıklama alanlarını doldurun.")

        # TODO Asil islemlerin kisimlari burada
        else:
            recete_id = get_highest_id('reçete', 'ReçeteID')
            recete_id += 1
            current_datetime = datetime.now()
            insert_query_recete = """
            INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID, aciklama)
            VALUES (%s,%s, %s, %s, %s)
            """
            params_recete = (str(recete_id), current_datetime, str(st.session_state.veteriner_id), str(st.session_state.hastaHayvan), aciklama)
            insert_data(insert_query_recete, params_recete)

            for i, prescription in enumerate(st.session_state.prescriptions):
                ilac_id = ilac_ids.get(prescription['ilac'])

                if ilac_id:
                    insert_query_icerir = """
                    INSERT INTO içerir (İlaçID, ReçeteID, doz)
                    VALUES (%s,%s, %s)
                    """
                    params_icerir = (str(ilac_id), recete_id, prescription['doz'])
                    insert_data(insert_query_icerir, params_icerir)

            st.session_state.prescriptions = [{'ilac': '', 'doz': 0}]
            st.session_state.page = st.session_state.prev_page
            st.rerun()

    if st.button("Geri"):
        st.session_state.prescriptions = [{'ilac': '', 'doz': 0}]
        st.session_state.page = st.session_state.prev_page
        st.rerun()


# Reçete yaz sayfası fonksiyonu
# TODO Burada seçtiğinin için alt tarafta bilgilerini gorecek 
# TODO Yazılacak Onemli Kısım Burası Kaldı
def all_appointments():
    st.title("Tüm Randevular")

    get_query_veteriner_randevular = """
    SELECT * FROM bil372_project.randevu r
    Join hayvansahibi hs on hs.kullanıcıID = r.sahipID
    Join hastahayvan hh on hh.sahipID = hs.kullanıcıID
    WHERE veterinerID = %s ;
    """
    params = (str(st.session_state.veteriner_id),)
    

    data = get_data(get_query_veteriner_randevular, params)

    selected_rows = pd.DataFrame()

    if data is not None and not data.empty:
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        
        # Remove columns containing 'ID'
        # df = df.loc[:, ~df.columns.str.contains('ID')]
        columns = df.columns.tolist()
        for i, col in enumerate(columns):
            if col == "İsim":
                columns[i] = "Sahip İsmi"
                break
        df.columns = columns

        # Create a GridOptionsBuilder instance
        gb = GridOptionsBuilder.from_dataframe(df)
        # Configure selection and layout options
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
        gb.configure_column("Tarih", filter="agDateColumnFilter")
        gridOptions = gb.build()

        # Display the grid with selectable rows
        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode='MODEL_CHANGED',
            enable_enterprise_modules=True, 
            width='100%',
            height=200,
        )
        selected_rows = grid_response['selected_rows']

    else:
        st.warning("Randevu Bulunamadı.")

    if selected_rows is not None and not selected_rows.empty:
        st.write('Review')
        get_query_veteriner_review = """
        SELECT *
        FROM bil372_project.reviewverir rv
        WHERE HayvanSahibiID = %s and VeterinerID = %s and Anonim = False;
        """
        params = (str(selected_rows['SahipID'].iloc[0]), str(selected_rows['VeterinerID'].iloc[0]))
        
        data = get_data(get_query_veteriner_review, params)

        st.write(data)

    if selected_rows is not None and not selected_rows.empty:
        st.write('Reçete')

        get_query_veteriner_recete = """
        SELECT *
        FROM bil372_project.reçete r
        WHERE VeterinerID = %s and HastaHayvanID = %s and Tarih between %s and %s;
        """
        tarih_value = pd.to_datetime(selected_rows['Tarih'].iloc[0])
        params = (str(selected_rows['VeterinerID'].iloc[0]), str(selected_rows['HastaID'].iloc[0]), tarih_value , tarih_value + timedelta(days=7))
        print(str(selected_rows['VeterinerID'].iloc[0]))
        print(str(selected_rows['HastaID'].iloc[0]))
        print(selected_rows['Tarih'].iloc[0])
        data2 = get_data(get_query_veteriner_recete, params)

        st.write(data2)
        
        if data2 is not None and not data2.empty:
            st.write('Reçetedeki İlaçlar')
            get_query_veteriner_recete_ilaclar = """
            SELECT *
            FROM bil372_project.içerir i
            Natural Join bil372_project.ilaçlar
            WHERE ReçeteID = %s;
            """
            tarih_value = pd.to_datetime(selected_rows['Tarih'].iloc[0])
            params3 = (str(data2['ReçeteID'].iloc[0]),)
            data3 = get_data(get_query_veteriner_recete_ilaclar, params3)
            st.write(data3)


    # TODO Buna basinca geri sayfada biraz bozuluyor düzeltilebilir.   
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
