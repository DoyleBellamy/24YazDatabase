import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time, delete_data
from ilacEkleme import add_medicine_page
import GeneralUser as g
from st_aggrid import AgGrid, GridOptionsBuilder

# Admin ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - admin_main_page
#   - addD_veterinarian_page
#   - add_veterinarian_avaliable_time_page
#   - admin_info_page

def admin_main_page():
    st.title("Admin Ana Sayfa")
    
    
    # Fetch veterinarians data from the database
    veterinarians_query = """
    SELECT veteriner.KullanıcıID, İsim, Soyisim, Email, TelefonNo
    FROM veteriner
    JOIN kullanıcı ON veteriner.KullanıcıID = kullanıcı.KullanıcıID
    """
    veterinarians_data = get_data(veterinarians_query)
    
    selected_rows = pd.DataFrame()

    if veterinarians_data is not None and not veterinarians_data.empty:
        st.write("Veterinerler Listesi ve Bilgileri")
        # Convert data to a DataFrame
        df = pd.DataFrame(veterinarians_data)
        
    
        # Create a GridOptionsBuilder instance
        gb = GridOptionsBuilder.from_dataframe(df)
        # Configure selection and layout options
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
        gb.configure_grid_options(domLayout='autoHeight')
        
        gridOptions = gb.build()

        # Display the grid with selectable rows
        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode='MODEL_CHANGED',
            fit_columns_on_grid_load=True,
            enable_enterprise_modules=True, 
            width='100%',
        )

        selected_rows = grid_response['selected_rows']

    

    medicine_query = """
    SELECT İlaçID, İsim, Miktar
    FROM ilaçlar
    """
    medicine_data = get_data(medicine_query)

    if medicine_data is not None and not medicine_data.empty:
        st.write("İlaç Listesi ve Bilgileri")
        df_meds = pd.DataFrame(medicine_data)

        gb_meds = GridOptionsBuilder.from_dataframe(df_meds)
        gb_meds.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
        gb_meds.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)  # Enable pagination
        gb_meds.configure_grid_options(domLayout='normal')  # Change from autoHeight to normal to better handle pagination

        gridOptions_meds = gb_meds.build()

        grid_response_meds = AgGrid(
            df_meds,
            gridOptions=gridOptions_meds,
            update_mode='MODEL_CHANGED',
            fit_columns_on_grid_load=True,
            enable_enterprise_modules=True,
            height=350,  # Set a fixed height to ensure the grid does not extend too far
            width='100%',
        )

        selected_meds = grid_response_meds['selected_rows']

    
    

    col1, col2, col3, col4 = st.columns([6, 4, 4, 6])
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
    # Buraya onaylama eklenebilir ama arayüz işi olduğu için gerekli değil
    with col4:
        if selected_rows is not None and not selected_rows.empty:
            if st.button("Sil"):
                delete_query = "DELETE FROM veteriner WHERE KullanıcıID = %s"
                id = str(selected_rows['KullanıcıID'][0])
                delete_data(delete_query, (id,))
                st.rerun()  # Refresh the page to reflect the changes
        if selected_meds is not None and not selected_meds.empty:
            if st.button("Sil"):
                delete_query = "DELETE FROM ilaçlar WHERE İlaçID = %s"
                ilac_id = str(selected_meds['İlaçID'][0]  )
                delete_data(delete_query, (ilac_id,))
                st.rerun()
        
    

# Veteriner hekim ekle sayfası fonksiyonu
# TODO yeni bir veteriner ve kullanıcı entitysi yarattığımız için rol ve email inputları da alınmalı
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
    veteriner_email = st.text_input("Email")
    veteriner_sifre = st.text_input("Şifre")
    
    # TC Kimlik Numarası
    #veteriner_tcno = st.number_input("TC Kimlik Numarası", value=None, format="%.0f")
    veteriner_tcno = st.text_input("TC Kimlik Numarası")
    if veteriner_tcno and not g.is_valid_tc(veteriner_tcno):
        st.error("TC Kimlik Numarası 11 haneli bir sayı olmalıdır.")

    # Telefon Numarası
    veteriner_telno =st.text_input("Telefon Numarası")
    if veteriner_telno and not g.is_valid_tel(veteriner_telno):
        st.error("Geçersiz telefon numarası.")

    
    veteriner_sehir = st.text_input("Şehir")
    veteriner_ilce =st.text_input("İlçe")
    veteriner_mahalle =st.text_input("Mahalle")
    veteriner_odano =st.text_input("Oda Numarası")
    # Uygun saat idleri her yerden ulaşılır olması lazım add_veterinarian_page içinde
    tum_idler = []
    with st.popover("Veteriner haftalık çalışma saatler"):
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
        
        #Uygunluk saatleri tüm idlerde tutuluyor ve veteriner ekleme işlemi bitirildikten sonra tcnoya göre veteriner idsi bulunup uygunluk saati
        #insert ediliyor
        true_values = [(row, col) for row in df.index for col in calendar_data_modified.columns if calendar_data_modified.at[row, col] == True]
            
        for day, time in true_values:
            formatted_time = format_time(time)
            saatler_query = """
            SELECT SaatID FROM bil372_project.saatler
            WHERE Saat = %s and Gün = %s;
            """
            params = (formatted_time, day)
            saat_idler_temp = get_data(query=saatler_query, params=params)
            birinci_sutun_degerleri = saat_idler_temp.iloc[:, 0].tolist()
            tum_idler.extend(birinci_sutun_degerleri)            
            
    if st.button("Ekle"):

        # Veteriner Kullanıcının childı olduğu için önce Kullanıcı entitysi insert edip sonra buna bağlı bir veteriner entitysi yaratmak gerekiyor
        # IDyi get_highest_id yerine Kullanıcı insert ettikten sonra emaile göre bulursak daha doğru olur
        veteriner_id = int(get_highest_id('kullanıcı', 'KullanıcıID')) + 1
        
        # Kullanıcı için insert
        insert_query_kullanıcı = """
        INSERT INTO kullanıcı (Email, Şifre, Rol)
        VALUES (%s,%s, %s)
        """
        params1 = (veteriner_email,veteriner_sifre,"veteriner")
        insert_data(insert_query_kullanıcı,params1)

        #Veteriner için insert
        insert_query_veteriner = """
        INSERT INTO veteriner (KullanıcıID,İsim, Soyisim, TCNO, TelefonNo, İlçe, Mahalle, İl, OdaNO, AdminID)
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params2 = (veteriner_id,veteriner_isim, veteriner_soyisim, veteriner_tcno, ("0"+veteriner_telno), veteriner_ilce, veteriner_mahalle, veteriner_sehir, veteriner_odano, str(st.session_state.admin_id))

        insert_data(insert_query_veteriner, params2)

        query =  "SELECT * FROM bil372_project.veteriner where KullanıcıID = '{}'".format(veteriner_id)
        data = get_data(query)

        #Varsa saat Uygunluklarını ekle
        if (tum_idler ):
            insert_query_veteriner_uygunluk = """
                INSERT INTO uygundur (SaatID, VeterinerID)
                VALUES (%s, %s)
                    """
            for saat_id in tum_idler:
                params = (str(saat_id), veteriner_id)
                insert_data(insert_query_veteriner_uygunluk, params)
        # Veteriner Ekleninceki senaryo
        if data is not None and not data.empty:
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Admin Main"
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

    a_id = st.session_state.admin_id

    # Admin bilgilerini getir
    admin_info_query ="""
    SELECT * FROM kullanıcı WHERE KullanıcıID = '{}'
    """.format(a_id)

    admin_info = get_data(admin_info_query)

    email = admin_info.iloc[0]['Email']
    st.title("Bilgilerim")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()

    email = st.text_input("Email", value = email)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):

            update_admin_query = """
            UPDATE kullanıcı SET Email = %s WHERE KullanıcıID = %s
            """
            params = email, int( a_id)

            try:
               data1 = update_data(update_admin_query,params)
            except:
                st.error("Email adresiniz değiştirilirken bir hata oluştu.")
            else:
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database
    with col2:
        if st.button("Şifreyi Değiştir"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Admin Change Password"
            st.rerun()

def admin_change_password_page():
    g.change_password_page(st.session_state.admin_id)
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.session_state.prev_page = "Admin Main"
        st.rerun()