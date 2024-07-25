import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g

# Admin ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - admin_main_page
#   - addD_veterinarian_page
#   - add_veterinarian_avaliable_time_page
#   - admin_info_page

def admin_main_page():
    st.title("Admin Ana Sayfa")
    st.write("Hayvanlar Listesi ve Bilgileri")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Veteriner Hekim Ekle"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Add Veterinarian"
            st.rerun()
    with col2:
        if st.button("İlaç Ekle"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Add Medicine"
            st.rerun()
    with col3:
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Admin Info"
            st.rerun()

# Veteriner hekim ekle sayfası fonksiyonu

# TODO Burada hem Veteriner bilgilerinin alındığından hem de uygundur ilişkisi üzerinden saatlerle bağlı olduğundan emin olmalıyız
# TODO Burada uygunluk saatlerini eklemeyeceğiz. Sonraki sayfada bunu yapacağız
# Yapılmadıysa kontrol edilmeli

def add_veterinarian_page():
    st.title("Veteriner Hekim Ekle")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    veteriner_isim = st.text_input("İsim")
    veteriner_soyisim = st.text_input("Soyisim")
    
    # TC Kimlik Numarası
    #veteriner_tcno = st.number_input("TC Kimlik Numarası", value=None, format="%.0f")
    veteriner_tcno = st.text_input("TC Kimlik Numarası")
    if veteriner_tcno and not g.is_valid_tc(veteriner_tcno):
        st.error("TC Kimlik Numarası 11 haneli bir sayı olmalıdır.")

    # Telefon Numarası
    #veteriner_telno = st.number_input("Telefon Numarası", value=None, format="%.0f", placeholder="5__")
    veteriner_telno ="0"+ st.text_input("Telefon Numarası")
    if veteriner_telno and not g.is_valid_tel(veteriner_telno):
        st.error("Geçersiz telefon numarası.")

    
    
    veteriner_sehir = st.text_input("Şehir")
    veteriner_ilce =st.text_input("İlçe")
    veteriner_mahalle =st.text_input("Mahalle")
    veteriner_odano =st.text_input("Oda Numarası")

    with st.popover("Veteriner haftalık çalışma saatler"):
        #st.title("Veteriner Uygunluk Süreleri Ekleme")
        df = pd.DataFrame(
        [   
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False}
        ],index=["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        )
        calendar_data_modified = st.data_editor(df)
        print(calendar_data_modified)
        
        #TODO uygunluk saati boşken de kabul olucak şekilde kaydetmeye 2 farklı senaryo eklenicek
        #Uygunluk saatleri tüm idlerde tutuluyor ve veteriner ekleme işlemi bitirildikten sonra tcnoya göre veteriner idsi bulunup uygunluk saati
        #insert ediliyor
        tum_idler = []
        if st.button("Uygunluk Sürelerini Kaydet", key="large_button", use_container_width=True):
        # st.session_state.prev_page = st.session_state.page
            true_values = [(row, col) for row in df.index for col in calendar_data_modified.columns if calendar_data_modified.at[row, col] == True]
            
            for day, time in true_values:
                formatted_time = format_time(time)
                #TODO ekle tuşuna basınca olması gerekiyor veteriner eklenmeden bu eklenemez
                saatler_query = """
                SELECT SaatID FROM bil372_project.saatler
                WHERE Saat = %s and Gün = %s;
                """
                params = (formatted_time, day)
                saat_idler_temp = get_data(query=saatler_query, params=params)
                birinci_sutun_degerleri = saat_idler_temp.iloc[:, 0].tolist()
                tum_idler.extend(birinci_sutun_degerleri)            
            print("tüm idler")
            print(tum_idler)
            print("true valıues")
            print(true_values)
            print("saat idler temp")
            print(saat_idler_temp)
            
            
    #if st.button("Geç"):
    #    st.session_state.page = "Veterinarian Add Times Avaliable"
    #    st.rerun()
    if st.button("Ekle"):
        veteriner_id = int(get_highest_id('kullanıcı', 'KullanıcıID')) + 1

        insert_query_veteriner = """
        INSERT INTO veteriner (KullanıcıID,İsim, Soyisim, TCNO, TelefonNo, İlçe, Mahalle, İl, OdaNO, AdminID)
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        print("admin id")
        print(st.session_state.admin_id)
        #params = (str(veteriner_id), veteriner_isim, veteriner_soyisim, veteriner_tcno, str(veteriner_telno), veteriner_ilce, veteriner_mahalle, veteriner_sehir, veteriner_odano, str(st.session_state.admin_id))
        params = (veteriner_id,veteriner_isim, veteriner_soyisim, veteriner_tcno, str(veteriner_telno), veteriner_ilce, veteriner_mahalle, veteriner_sehir, veteriner_odano, str(st.session_state.admin_id))

        insert_data(insert_query_veteriner, params)

        query =  "SELECT * FROM bil372_project.veteriner where KullanıcıID = '{}'".format(veteriner_id)
        data = get_data(query)
        if (tum_idler ):
            insert_query_veteriner_uygunluk = """
                INSERT INTO uygundur (SaatID, VeterinerID)
                VALUES (%s, %s)
                    """
            for saat_id in tum_idler:
                params = (str(saat_id), str(st.session_state.veteriner_id))
                insert_data(insert_query_veteriner_uygunluk, params)
        # Veteriner Ekleninceki senaryo
        if data is not None and not data.empty:
            #st.session_state.veteriner_id_added = data.iloc[0]['KullanıcıID'] 

            st.session_state.prev_page = st.session_state.page
            #st.session_state.page = "Veterinarian Add Times Avaliable"
            st.rerun()

        # Veteriner Eklenmeyince Error ver
        else:
            st.error("Girdiğiniz Bilgilerde Hata var tekrar kontrol edin")

# Burada havali bir tablo olacak
# TODO BURADA 1 tur uygunluk eklendi deyip sonrasında pop-up ile sonrasında bu popup'dan ilerle deyince admin sayfasına geçme işlemi gerçekleştirilebilir.
# TODO bu sayede veteriner_added state'i de silinebilir
# TODO Bu sayfa direk veteriner ekleme kısmı yerine kendi kısmına çekilebilir veteriner bilgilerini adminden değiştirdiğimizi varsayarsak, fakat şuan veteriner
# kendi değiştirebiliyor veteriner info admine çekilebilir
def add_veterinarian_avaliable_time_page():
    st.title("Veteriner Uygunluk Süreleri Ekleme")
    #Hepsinin default'ını false'a çek
    df = pd.DataFrame(
        [   
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False},
        { "09.00": False, "10.00": False, "11.00": False, "13.00": False, "14.00": False, "15.00": False, "16.00": False, "17.00": False}
        ],index=["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
    )

    # DataFrame'i göster
    calendar_data_modified = st.data_editor(df)
    print(calendar_data_modified)
    
    # TODO Buradaki Prev_pages'e karar verilecek Belki olmayadabilir
    if st.button("Uygunluk Sürelerini Kaydet", key="large_button", use_container_width=True):
        # st.session_state.prev_page = st.session_state.page
        true_values = [(row, col) for row in df.index for col in calendar_data_modified.columns if calendar_data_modified.at[row, col] == True]
        tum_idler = []
        for day, time in true_values:

            formatted_time = format_time(time)

            #Tabloya göre idyi getiriyor
            saatler_query = """
            SELECT SaatID FROM bil372_project.saatler
            WHERE Saat = %s and Gün = %s;
            """
            params = (formatted_time, day)
            saat_idler_temp = get_data(query=saatler_query, params=params)
            birinci_sutun_degerleri = saat_idler_temp.iloc[:, 0].tolist()
            tum_idler.extend(birinci_sutun_degerleri)            
        print(tum_idler)
        print(true_values)
        print("saat idler temp" + saat_idler_temp)
        
        insert_query_veteriner_uygunluk = """
        INSERT INTO uygundur (SaatID, VeterinerID)
        VALUES (%s, %s)
                """
        for saat_id in tum_idler:
            params = (str(saat_id), str(st.session_state.veteriner_id_added))
            insert_data(insert_query_veteriner_uygunluk, params)

        st.session_state.page = "Admin Main"
        st.rerun()

    #TODO Burada gunlerin hepsini secmek icin olan kod eklenecek
    # 5 tane butonla bunu halledecegiz ama sonraki is 

    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     state_pazartesi = True
    #     print(state_pazartesi)
    #     if st.button("Pazartesi"):
    #         if state_pazartesi:
    #             calendar_data_modified.loc["Pazartesi"] = True
    #             state_pazartesi = False
    #         else: 
    #             print(state_pazartesi)
    #             df.loc["Pazartesi"] = False

# Admin bilgileri sayfası fonksiyonu
def admin_info_page():
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