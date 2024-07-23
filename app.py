import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
#from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# st.session_state kullanarak kullanıcı_id tanımlama
if 'kullanıcı_id' not in st.session_state:
    st.session_state.kullanıcı_id = None

if 'rol' not in st.session_state:
    st.session_state.rol = None

if 'admin_id' not in st.session_state:
    st.session_state.admin_id = None

if 'veteriner_id' not in st.session_state:
    st.session_state.veteriner_id = None


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
            query =  "SELECT * FROM bil372_project.kullanıcı where email = '{}' and şifre = '{}' and rol ='{}'".format(mail, sifre,"veteriner")
            data = get_data(query)
            
            if data is not None and not data.empty:
                st.session_state.veteriner_id = data.iloc[0]['KullanıcıID'] 
                st.session_state.rol = 'Veteriner'

                st.session_state.prev_page = st.session_state.page
                st.session_state.page = "Veterinarian Main"
                st.experimental_rerun()
            else:
                st.write("Veteriner bulunamadı veya yanlış giriş bilgileri.")

            

    if st.button("Kayıt Ol"):
        st.session_state.prev_page = st.session_state.page
        st.session_state.page = "Register"
        st.experimental_rerun()

# Kayıt ol sayfası fonksiyonu
# TODO bu kısmın sıralaması duzeni biraz degisebilir
def register_page():
    st.title("Kullanıcı Kayıt Ol")
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

    if st.button("Kayıt Ol"):
        id = get_highest_id('kullanıcı', 'KullanıcıID')
        id = id + 1        
        insert_query_kullanici = """
        INSERT INTO kullanıcı (kullanıcıID, email, şifre, rol)
        VALUES (%s, %s, %s, %s)
        """
        params = (id, mail, sifre, 'kullanıcı')

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

# TODO DEĞİŞTİRDİ OLARAK GÖSTERİYOR TÜM IFLERI GEÇİYOR ANCAK get_data ÇAĞRILDIĞINDA ESKİ ŞİFRE GÖZÜKÜYOR
# Şifre değiştirme sayfası
def change_password_page():
    st.title("Şifre Değiştir")
    current_password = st.text_input("Mevcut Şifre", type="password")
    new_password = st.text_input("Yeni Şifre", type="password")
    confirm_password = st.text_input("Yeni Şifreyi Onayla", type="password")

    if st.button("Şifreyi Değiştir"):
        if new_password != confirm_password:
            st.error("Yeni şifreler uyuşmuyor.")
        else:
            user_id = (st.session_state.kullanıcı_id or 
                       st.session_state.admin_id or 
                       st.session_state.veteriner_id)
            if user_id is None:
                st.error("Kullanıcı kimliği bulunamadı.")
            else:
                user_id = int(user_id)  # Ensure user_id is an integer
                query = "SELECT şifre FROM bil372_project.kullanıcı WHERE KullanıcıID = '{}'".format(user_id)
                data = get_data(query)
                print("Select Query Data:", data)
                
                if data is not None and not data.empty and data.iloc[0]['şifre'] == current_password:
                    update_query = "UPDATE bil372_project.kullanıcı SET şifre = '{}' WHERE KullanıcıID = '{}'".format(new_password, user_id)
                    print("Update Query:", update_query)
                    update_data(update_query, (new_password, user_id))
                    st.write("Şifre Değiştirildi.")
                else:
                    st.error("Mevcut şifre yanlış.")

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

    # TODO silinecek
    print(animals_data)

    if animals_data is not None and not animals_data.empty:
        st.write("Hayvanların Bilgileri:")

        # Seçili satırları saklamak için bir liste
        selected_rows = []

        for index, row in animals_data.iterrows():
            # Sütunları oluştur
            cols = st.columns([1, 5, 1])  # 1: Checkbox için, 5: Satır Bilgisi için, 1: Buton için
            
            # Checkbox ve butonları ilgili sütunlara yerleştir
            with cols[0]:  # Checkbox sütunu
                if st.checkbox("", key=f"checkbox_{index}"):
                    selected_rows.append(index)
            
            with cols[1]:  # Satır bilgisi sütunu
                # Her satır için küçük bir tablo oluşturma
                st.write(pd.DataFrame([row], columns=animals_data.columns))
            
            #TODO BURADA SEÇİLEN Hayvan silme işlemi pop-up sonrası gerçekleşecek 
            with cols[2]:  # Buton sütunu
                if st.button(f"{row['HastaID']} Sil", key=f"button_{index}"):
                    st.write(f"{row['HastaID']} için butona tıklandı!")

        # BU KISIM BELKİ SİLİNEBİLİR
        # Seçili satırları gösterme
        if selected_rows:
            st.write("Seçili Satırlar:")
            selected_data = animals_data.loc[selected_rows]
            st.table(selected_data)

    col1, col2, col3 = st.columns(3)
    with col1:
        # Bu kısmın kodu eklendi hazır
        if st.button("Hayvan Ekle"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Add Animal"
            st.experimental_rerun()
    with col2:
        # TODO Bu kısım eklenecek. Hem bilgilerini görecek ve update de edebilmesi lazım
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Info Page"
            st.experimental_rerun()
    with col3:
        # TODO Burada checkbox ile seçilen 1 tane hayvan için randevu alacagiz
        # TODO Secili herhangi bir hayvan yoksa randevu ala bastığı durumda hata vericez
        if st.button("Randevu Al"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Book Appointment"
            st.experimental_rerun()

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)  # Add some space before the larger button

    # Bu günün tarihiyle randevu tarihini kıyaslayıp ekleyeceğiz
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
# TODO Bu sayfa da başka değişiklik yapılmayacaksa yeni .py dosyasına geçebilir
def add_animal_page():
    st.title("Hayvan Ekleme Ekrani")
    
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()

    hayvan_isim = st.text_input("İsim")
    hayvan_kilo = st.number_input("Kilo", min_value=0.0, step=0.1)
    hayvan_boy = st.number_input("Boy", min_value=0.0, step=0.1)
    hayvan_yaş = st.number_input("Yaş", min_value=0.0, step=0.1)
    hayvan_renk = st.text_input("Renk")
    hayvan_tur = st.selectbox("Tür", options=["Kedi", "Köpek", "Kuş", "Tavşan", "Kaplumbağa", "Hamster", "Kobay"])
    hayvan_cinsiyet = st.selectbox("Cinsiyet", options=["Dişi", "Erkek"])
    
    # TODO BURAYA EKLENDİ Mİ KONTROLLERİ YAPILIP USER MAIN PAGE'E GECİS YAPILACAK
    # TODO İlac ekleme sayfasina da ayni sekilde kontrol saglanmali
    # Ornek icin veteriner ekleme kismindaki koda bakilabilir
    if st.button("Ekle"):
        hayvan_id = get_highest_id('hastahayvan', 'HastaID')
        hayvan_id = hayvan_id + 1 

        insert_query_hastahayvan = """
        INSERT INTO hastahayvan (HastaID, SahipID, Yaş, Boy, İsim, Kilo, Tür, Cinsiyet)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (hayvan_id, str(st.session_state.kullanıcı_id), str(hayvan_yaş), str(hayvan_boy), str(hayvan_isim), str(hayvan_kilo), hayvan_tur, hayvan_cinsiyet)

        insert_data(insert_query_hastahayvan, params)

        if hayvan_renk is not None:
            insert_query_renkler = """
            INSERT INTO renkler (HayvanID, Renk)
            VALUES (%s, %s)
            """
            params = (hayvan_id, hayvan_renk)

            insert_data(insert_query_renkler, params)

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

# TODO Burada hem Veteriner bilgilerinin alındığından hem de uygundur ilişkisi üzerinden saatlerle bağlı olduğundan emin olmalıyız
# TODO Burada uygunluk saatlerini eklemeyeceğiz. Sonraki sayfada bunu yapacağız
# Yapılmadıysa kontrol edilmeli

def is_valid_tc(input_value):
    input_value = int(input_value)
    return len(str(input_value)) == 11

def is_valid_tel(input_value):
    input_value = int(input_value)
    return len(str(input_value)) == 10


def add_veterinarian_page():
    st.title("Veteriner Hekim Ekle")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()
    veteriner_isim = st.text_input("İsim")
    veteriner_soyisim = st.text_input("Soyisim")
    
    # TC Kimlik Numarası
    veteriner_tcno = st.number_input("TC Kimlik Numarası", value=None, format="%.0f")
    if veteriner_tcno and not is_valid_tc(veteriner_tcno):
        st.error("TC Kimlik Numarası 11 haneli bir sayı olmalıdır.")

    # Telefon Numarası
    veteriner_telno = st.number_input("Telefon Numarası", value=None, format="%.0f", placeholder="5__")
    if veteriner_telno and not is_valid_tel(veteriner_telno):
        st.error("Geçersiz telefon numarası.")

    
    
    veteriner_sehir = st.text_input("Şehir")
    veteriner_ilce =st.text_input("İlçe")
    veteriner_mahalle =st.text_input("Mahalle")
    veteriner_odano =st.text_input("Oda Numarası")

    if st.button("Geç"):
        st.session_state.page = "Veterinarian Add Times Avaliable"
        st.experimental_rerun()
    if st.button("Ekle"):
        veteriner_id = get_highest_id('veteriner', 'KullanıcıID') + 1

        insert_query_veteriner = """
        INSERT INTO veteriner (KullanıcıID, İsim, Soyisim, TCNO, TelefonNo, İlçe, Mahalle, İl, OdaNO, AdminID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (str(veteriner_id), veteriner_isim, veteriner_soyisim, str(veteriner_tcno), str(veteriner_telno), veteriner_ilce, veteriner_mahalle, veteriner_sehir, veteriner_odano, str(st.session_state.admin_id))

        insert_data(insert_query_veteriner, params)

        query =  "SELECT * FROM bil372_project.veteriner where KullanıcıID = '{}'".format(veteriner_id)
        data = get_data(query)
        
        # Veteriner Ekleninceki senaryo
        if data is not None and not data.empty:
            st.session_state.veteriner_id_added = data.iloc[0]['KullanıcıID'] 

            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Veterinarian Add Times Avaliable"
            st.experimental_rerun()

        # Veteriner Eklenmeyince Error ver
        else:
            st.error("Girdiğiniz Bilgilerde Hata var tekrar kontrol edin")


# Burada havali bir tablo olacak
# TODO BURADA 1 tur uygunluk eklendi deyip sonrasında pop-up ile sonrasında bu popup'dan ilerle deyince admin sayfasına geçme işlemi gerçekleştirilebilir.
# TODO bu sayede veteriner_added state'i de silinebilir
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
        insert_query_veteriner_uygunluk = """
        INSERT INTO uygundur (SaatID, VeterinerID)
        VALUES (%s, %s)
                """
        for saat_id in tum_idler:
            params = (str(saat_id), str(st.session_state.veteriner_id_added))
            insert_data(insert_query_veteriner_uygunluk, params)

        st.session_state.page = "Admin Main"
        st.experimental_rerun()

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
        st.experimental_rerun()

    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        tc_kimlik_no = st.number_input("TC Kimlik No", value=None, format="%.0f")
        if tc_kimlik_no and not is_valid_tc(tc_kimlik_no):
            st.error("TC kimlik numarası 11 haneli olmalıdır.")

    with col2:
        email_adresi = st.text_input("E-Mail Adresi")
        telefon = st.number_input("Telefon Numarası", value=None, format="%.0f", placeholder="5__")
        if telefon and not is_valid_tel(telefon):
            st.error("Geçersiz telefon numarası.")
        adres = st.text_input("Adres")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):
            if is_valid_tc(tc_kimlik_no) and is_valid_tel(telefon):
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database
            else:
                st.error("Lütfen bilgileri doğru formatta girin.")

def veterinarian_info_page():
    st.title("Bilgilerim")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.experimental_rerun()

    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        tc_kimlik_no = st.number_input("TC Kimlik No", value=None, format="%.0f")
        if tc_kimlik_no and not is_valid_tc(tc_kimlik_no):
            st.error("TC kimlik numarası 11 haneli olmalıdır.")

    with col2:
        email_adresi = st.text_input("E-Mail Adresi")
        telefon = st.number_input("Telefon Numarası", value=None, format="%.0f", placeholder="5__")
        if telefon and not is_valid_tel(telefon):
            st.error("Geçersiz telefon numarası.")
        adres = st.text_input("Adres")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):
            if is_valid_tc(tc_kimlik_no) and is_valid_tel(telefon):
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database
            else:
                st.error("Lütfen bilgileri doğru formatta girin.")
    with col2:
        if st.button("Şifreyi Değiştir"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Change Password"
            st.experimental_rerun()

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
            st.session_state.page = "Info Page"
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
elif st.session_state.page == "Veterinarian Add Times Avaliable":
    add_veterinarian_avaliable_time_page()
elif st.session_state.page == "Info Page":
    veterinarian_info_page()
elif st.session_state.page == "Change Password":
    change_password_page()
