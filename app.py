import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data


# st.session_state kullanarak kullanıcı_id tanımlama
if 'kullanıcı_id' not in st.session_state:
    st.session_state.kullanıcı_id = None

if 'rol' not in st.session_state:
    st.session_state.rol = None

if 'admin_id' not in st.session_state:
    st.session_state.admin_id = None



# Ana sayfa fonksiyonu
def main_page():
    st.title("Ana Sayfa")
    st.write("Bu, ana sayfanızdır.")
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://i.pinimg.com/564x/5e/16/49/5e1649c42a84d94f7a98535ec85f0ac6.jpg"  style="width: 350px;"/>
        </div>
        """,
        unsafe_allow_html=True
    )
    mail = st.text_input("Mail Adresi", key="login_email")
    sifre = st.text_input("Şifre", type="password", key="login_password")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Hasta Girişi"):
            query =  "SELECT * FROM bil372_project.kullanıcı where email = '{}' and şifre = '{}' and rol ='{}'".format(mail, sifre,"kullanıcı")
            data = get_data(query)
            
            if data is not None and not data.empty:
                st.session_state.kullanıcı_id = data.iloc[0]['KullanıcıID'] 
                st.session_state.rol = 'Kullanici'

                st.session_state.prev_page = st.session_state.page
                st.session_state.page = "User Main"
                st.experimental_rerun()
            else:
                st.write("Kullanıcı bulunamadı veya yanlış giriş bilgileri.")


    with col2:
        if st.button("Admin Giriş"):
            query =  "SELECT * FROM bil372_project.kullanıcı where email = '{}' and şifre = '{}' and rol ='{}'".format(mail, sifre,"admin")
            data = get_data(query)   
            if data is not None and not data.empty:
                st.session_state.admin_id = data.iloc[0]['KullanıcıID'] 
                st.session_state.rol = 'Admin'

                st.session_state.prev_page = st.session_state.page
                st.session_state.page = "Admin Main"
                st.experimental_rerun()
            else:
                st.write("Admin bulunamadı veya yanlış giriş bilgileri.")

            
    
    with col3:
        if st.button("Veteriner Hekim Giriş"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Veterinarian Main"
            st.experimental_rerun()

    if st.button("Kayıt Ol"):
        st.session_state.prev_page = st.session_state.page
        st.session_state.page = "Register"
        st.experimental_rerun()

# Kayıt ol sayfası fonksiyonu
# TODO bu kısmın sıralaması duzeni biraz degisebilir
def register_page():
    st.title("Kayıt Ol")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    mail = st.text_input("Mail Adresi", key="register_email")
    sifre = st.text_input("Şifre", type="password", key="register_password")
    isim = st.text_input("İsim", key="register_name")
    soyisim = st.text_input("Soyisim", key="register_surname")
    il = st.text_input("İl", key="register_city")
    ilce = st.text_input("İlce", key="register_suborb")
    mahalle = st.text_input("Mahalle", key="register_neighboor")

    # BU KISMI HANGI TURDEKI KAYITLARA IZIN VERECEGIMIZE GORE DEGISTIRECEGIZ
    rol = st.selectbox(
        'Kullanıcı türünü secin',
        ['kullanıcı', 'admin', 'veteriner']
    )
    if st.button("Kayıt Ol"):
        id = get_highest_id('kullanıcı', 'KullanıcıID')
        id = id + 1        
        insert_query_kullanici = """
        INSERT INTO kullanıcı (kullanıcıID, email, şifre, rol)
        VALUES (%s, %s, %s, %s)
        """
        params = (id, mail, sifre, rol)

        insert_data(insert_query_kullanici, params)

        
        insert_query_hayvan_sahibi = """
        INSERT INTO hayvansahibi (kullanıcıID, isim, soyisim, il, ilçe,mahalle)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (id, isim, soyisim, il, ilce, mahalle)
        insert_data(insert_query_hayvan_sahibi, params)
        st.session_state.prev_page = st.session_state.page
        st.session_state.page = "Ana Sayfa"
        st.experimental_rerun()

# Kullanıcı ana sayfa fonksiyonu
def user_main_page():
    st.title("Kullanıcı Ana Sayfa")
    st.write("Hayvanlar Listesi ve Bilgileri ve Randevu Alma")

    animal_query = """
    SELECT * FROM bil372_project.hastahayvan
    WHERE SahipID = %s;
    """
    id_str = str(st.session_state.kullanıcı_id)
    animals_data = get_data(animal_query, (id_str,))
    print(animals_data)

    if animals_data is not None and not animals_data.empty:
        st.table(animals_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Hayvan Ekle"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Add Animal"
            st.experimental_rerun()
    with col2:
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "User Info"
            st.experimental_rerun()
    with col3:
        if st.button("Randevu Al"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Book Appointment"
            st.experimental_rerun()

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)  # Add some space before the larger button

    if st.button("Geçmiş Randevularım", key="large_button", help="Geçmiş Randevuları Görüntüle", use_container_width=True):
        st.session_state.prev_page = st.session_state.page
        st.session_state.page = "Past Appointments"
        st.experimental_rerun()

# Geçmiş randevular sayfası fonksiyonu
def past_appointments_page():
    st.title("Geçmiş Randevular")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.write("Geçmiş Randevu, Review, Fatura Bilgileri, Reçete")

# Kullanıcı bilgileri sayfası fonksiyonu
def user_info_page():
    st.title("Bilgilerim")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.write("Doktor ve Uygun Saatler Listesi")

# Hayvan ekle sayfası fonksiyonu
def add_animal_page():
    st.title("Hayvan Ekle")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.text_input("Tür")
    st.number_input("Kilo", min_value=0.0, step=0.1)
    st.number_input("Boy", min_value=0.0, step=0.1)
    st.selectbox("Cinsiyet", options=["Dişi", "Erkek"])
    if st.button("Ekle"):
        st.write("Hayvan eklendi!")  # Placeholder for adding animal to the database

# Randevu al sayfası fonksiyonu
def book_appointment_page():
    st.title("Randevu Al")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.write("Doktor ve Uygun Saatler Listesi")
    if st.button("Randevu Al"):
        # Placeholder for booking an appointment
        st.write("Randevu Al Buton")

# Admin ana sayfa fonksiyonu
def admin_main_page():
    st.title("Admin Ana Sayfa")
    st.write("Hayvanlar Listesi ve Bilgileri")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Veteriner Hekim Ekle"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Add Veterinarian"
            st.experimental_rerun()
    with col2:
        if st.button("İlaç Ekle"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Add Medicine"
            st.experimental_rerun()
    with col3:
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Admin Info"
            st.experimental_rerun()

# Veteriner hekim ekle sayfası fonksiyonu
def add_veterinarian_page():
    st.title("Veteriner Hekim Ekle")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.text_input("Mail Adresi")
    st.text_input("İsim")
    st.text_input("Soyisim vs.")
    if st.button("Ekle"):
        st.write("Veteriner hekim eklendi!")  # Placeholder for adding veterinarian to the database

# İlaç ekle sayfası fonksiyonu
def add_medicine_page():
    st.title("İlaç Ekle")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    ilac_ad = st.text_input("İlaç Adı")
    ilac_toplam_ucret = st.text_input("Toplam Ücret")
    ilac_miktar = st.text_input("Miktar")

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

# Admin bilgileri sayfası fonksiyonu
def admin_info_page():
    st.title("Bilgilerim")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()

    def validate_tc_kimlik_no(tc_kimlik_no):
        return re.fullmatch(r'\d{11}', tc_kimlik_no) is not None

    def validate_telefon(telefon):
        return re.fullmatch(r'\(\+90\) 05\d{9}', telefon) is not None

    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        tc_kimlik_no = st.text_input("T.C. Kimlik no", max_chars=11)

    with col2:
        email_adresi = st.text_input("E-Mail Adresi")
        telefon = st.text_input("Telefon", value="(+90) 05")
        adres = st.text_input("Adres")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):
            if validate_tc_kimlik_no(tc_kimlik_no) and validate_telefon(telefon):
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database
            else:
                st.error("Lütfen bilgileri doğru formatta girin.")
    with col2:
        if st.button("Şifreyi Değiştir"):
            st.write("Şifre değiştirme functionality to be implemented.")  # Placeholder for changing password

# Veteriner ana sayfa fonksiyonu
def veterinarian_main_page():
    st.title("Veteriner Ana Sayfa")
    st.write("Aktif Randevular")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Reçete Yaz"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Write Prescription"
            st.experimental_rerun()
    with col2:
        if st.button("Geçmiş Hastalar"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Past Patients"
            st.experimental_rerun()
    with col3:
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Admin Info"
            st.experimental_rerun()

# Reçete yaz sayfası fonksiyonu
def write_prescription_page():
    st.title("Reçete Yaz")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.selectbox("Hastalar", options=["Hasta 1", "Hasta 2"])  # Placeholder options
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("İlaç")
    with col2:
        st.text_area("Doz")
    st.text_area("Açıklama")
    if st.button("Reçeteyi Onayla"):
        st.write("Reçete onaylandı!")  # Placeholder for prescription approval

# Geçmiş hastalar sayfası fonksiyonu
def past_patients_page():
    st.title("Geçmiş Hastalar")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    st.write("Geçmiş Hastalar Listesi (Hastayı seçer, geçmiş bilgiler görüntülenir)")

# Başlangıçta session state'i ayarla
if 'page' not in st.session_state:
    st.session_state.page = "Ana Sayfa"
    st.session_state.prev_page = None

# Seçilen sayfayı göster
if st.session_state.page == "Ana Sayfa":
    main_page()
elif st.session_state.page == "Register":
    register_page()
elif st.session_state.page == "User Main":
    user_main_page()
elif st.session_state.page == "Past Appointments":
    past_appointments_page()
elif st.session_state.page == "User Info":
    user_info_page()
elif st.session_state.page == "Add Animal":
    add_animal_page()
elif st.session_state.page == "Book Appointment":
    book_appointment_page()
elif st.session_state.page == "Admin Main":
    admin_main_page()
elif st.session_state.page == "Add Veterinarian":
    add_veterinarian_page()
elif st.session_state.page == "Add Medicine":
    add_medicine_page()
elif st.session_state.page == "Admin Info":
    admin_info_page()
elif st.session_state.page == "Veterinarian Main":
    veterinarian_main_page()
elif st.session_state.page == "Write Prescription":
    write_prescription_page()
elif st.session_state.page == "Past Patients":
    past_patients_page()
