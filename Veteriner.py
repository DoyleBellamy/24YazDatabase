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


    get_query_veteriner_randevular = """
    SELECT * FROM bil372_project.randevu r
    Join hayvansahibi hs on hs.kullanıcıID = r.sahipID
    Join hastahayvan hh on hh.sahipID = hs.kullanıcıID
    WHERE veterinerID = %s;
    """
    params = (str(st.session_state.veteriner_id),)

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
        st.write("Selected Rows")
        st.write(selected_rows)

    else:
        st.write("Randevu Bulunamadı.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Reçete Yaz"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Write Prescription"
            st.rerun()
    with col2:
        # TODO Burada ismi değişen buton olacak. Aktif'ken sadece aktifler görünecek. Bir daha basınca tümü görünecek. 
        # Aktiften kasıt randevu tarihinin bugünden sonra olması diyebiliriz direkt
        if st.button("Tüm Randevular/Hastalar"):
            print("dummy")
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
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()

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

def veterinarian_change_password_page():
    g.change_password_page(st.session_state.veteriner_id)
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.session_state.prev_page = "Veterinarian Main"
        st.rerun()

# Reçete yaz sayfası fonksiyonu
def write_prescription_page():
    st.title("Reçete Yaz")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    st.selectbox("Hastalar", options=["Hasta 1", "Hasta 2"])  # Placeholder options
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("İlaç")
    with col2:
        st.text_area("Doz")
    st.text_area("Açıklama")
    if st.button("Reçeteyi Onayla"):
        st.write("Reçete onaylandı!")  # Placeholder for prescription approval
