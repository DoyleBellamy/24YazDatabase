import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g
from st_aggrid import AgGrid, GridOptionsBuilder

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
    WHERE veterinerID = %s and r.Tarih >= DATE_SUB(CURDATE(), INTERVAL 10 DAY);
    """
    params = (str(st.session_state.veteriner_id),)
    
    selected_rows = pd.DataFrame()

    data = get_data(get_query_veteriner_randevular, params)
    if data is not None and not data.empty:
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        
        # Remove columns containing 'ID'
        df = df.loc[:, ~df.columns.str.contains('ID')]
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
        gb.configure_grid_options(domLayout='autoHeight')
        
        gb.configure_column("Tarih", filter="agDateColumnFilter")
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

    else:
        st.warning("Randevu Bulunamadı.")

    # Burada hizalamalar yapılabilir
    col1, col2, col3 = st.columns(3)
    with col1:
        if selected_rows is not None and not selected_rows.empty:
            if st.button("Reçete Yaz"):
                st.session_state.prev_page = st.session_state.page
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



def write_prescription_page():
    st.title("Reçete Yaz")

    if 'prescriptions' not in st.session_state:
        st.session_state.prescriptions = [{'ilac': '', 'doz': ''}]

    # İlaç ve doz alanlarını dinamik olarak ekle
    for i, prescription in enumerate(st.session_state.prescriptions):
        col1, col2 = st.columns(2)
        with col1:        
            st.session_state.prescriptions[i]['ilac'] = st.text_input(f"İlaç {i+1}", prescription['ilac'], key=f'ilac_{i}')
        with col2:
            st.session_state.prescriptions[i]['doz'] = st.text_input(f"Doz {i+1}", prescription['doz'], key=f'doz_{i}')
    
    # Yeni ilaç ve doz alanı eklemek için buton
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Arttır"):
            st.session_state.prescriptions.append({'ilac': '', 'doz': ''})
    
    # İlaç ve doz alanlarını azaltmak için buton
    with col2:
        if st.button("Azalt"):
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
        else:
            st.write("Reçete onaylandı!")
            
            # İlaç ve doz bilgilerini bastır
            st.write("İlaç ve Doz Bilgileri:")
            for i, prescription in enumerate(st.session_state.prescriptions):
                st.write(f"İlaç {i+1}: {prescription['ilac']}")
                st.write(f"Doz {i+1}: {prescription['doz']}")
            
            # Açıklama bilgisini bastır
            st.write("Açıklama:")
            st.write(aciklama)

    if st.button("Geri"):
        st.session_state.prescriptions = [{'ilac': '', 'doz': ''}]
        st.session_state.page = st.session_state.prev_page
        st.rerun()



# Reçete yaz sayfası fonksiyonu
# TODO Burada seçtiğinin için alt tarafta bilgilerini gorecek 
def all_appointments():
    st.title("Tüm Randevular")

    get_query_veteriner_randevular = """
    SELECT * FROM bil372_project.randevu r
    Join hayvansahibi hs on hs.kullanıcıID = r.sahipID
    Join hastahayvan hh on hh.sahipID = hs.kullanıcıID
    WHERE veterinerID = %s ;
    """
    params = (str(st.session_state.veteriner_id),)
    
    selected_rows = pd.DataFrame()

    data = get_data(get_query_veteriner_randevular, params)
    if data is not None and not data.empty:
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        
        # Remove columns containing 'ID'
        df = df.loc[:, ~df.columns.str.contains('ID')]
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
        gb.configure_grid_options(domLayout='autoHeight')
        
        gb.configure_column("Tarih", filter="agDateColumnFilter")
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

    else:
        st.warning("Randevu Bulunamadı.")

    # TODO Buna basinca geri sayfada biraz bozuluyor düzeltilebilir.   
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
