import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time
from ilacEkleme import add_medicine_page
import GeneralUser as g

# Kullanıcı ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - user_main_page 
#   - past_appointments_page
#   - user_info_page
#   - add_animal_page
#   - book_appointment_page

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
            st.rerun()
    with col2:
        # TODO Bu kısım eklenecek. Hem bilgilerini görecek ve update de edebilmesi lazım
        if st.button("Bilgilerim"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "User Info"
            st.rerun()
    with col3:
        # TODO Burada checkbox ile seçilen 1 tane hayvan için randevu alacagiz
        # TODO Secili herhangi bir hayvan yoksa randevu ala bastığı durumda hata vericez
        if st.button("Randevu Al"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Book Appointment"
            st.rerun()

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)  # Add some space before the larger button

    # Bu günün tarihiyle randevu tarihini kıyaslayıp ekleyeceğiz
    if st.button("Geçmiş Randevularım", key="large_button", help="Geçmiş Randevuları Görüntüle", use_container_width=True):
        st.session_state.prev_page = st.session_state.page
        st.session_state.page = "Past Appointments"
        st.rerun()

# Geçmiş randevular sayfası fonksiyonu
def past_appointments_page():
    st.title("Geçmiş Randevular")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    st.write("Geçmiş Randevu, Review, Fatura Bilgileri, Reçete")

# Kullanıcı bilgileri sayfası fonksiyonu
def user_info_page():
    st.title("Bilgilerim")
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    
    #Kullanıcı bilgilerini getir
    user_query = """
    SELECT * FROM hayvansahibi AS h INNER JOIN kullanıcı AS k ON h.KullanıcıID = h.KullanıcıID WHERE k.KullanıcıID = '{}'
    """.format(st.session_state.kullanıcı_id)

    user_info = get_data(user_query)

    # Queryden gelen datadan ilgili bilgileri çek
    email_adresi = user_info.iloc[0]['Email']
    isim = user_info.iloc[0]['İsim']
    soyisim = user_info.iloc[0]['Soyisim']
    ilce =user_info.iloc[0]['İlçe']
    mah = user_info.iloc[0]['Mahalle']
    il = user_info.iloc[0]['İl']

    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("İsim", value = isim)
        soyisim = st.text_input("Soyisim", value = soyisim)
        ilce = st.text_input("İlce", value = ilce)

    with col2:
        email_adresi = st.text_input("E-Mail Adresi", value = email_adresi)
        il = st.text_input("İl", value = il)
        mah = st.text_input("Mahalle", value = mah)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Kaydet"):
            k_id = st.session_state.kullanıcı_id

            update_kul_query = """
            UPDATE kullanıcı SET Email = %s WHERE KullanıcıID = %s
            """
            params1 = email_adresi, int( k_id)

            update_sahip_query = """
            UPDATE hayvansahibi SET İsim = %s, Soyisim = %s, İl = %s, İlçe = %s, Mahalle = %s WHERE KullanıcıID = %s
            """ 

            params2 = isim, soyisim, il, ilce, mah,int( k_id)

            print("Here we go!")
            data1 = update_data(update_kul_query,params1)
            print(data1)
            data2 = update_data(update_sahip_query,params2)
            print(data2)
            if 1:
                st.write("Bilgileriniz güncellendi!")  # Placeholder for updating info in the database
            else:
                st.error("Lütfen bilgileri doğru formatta girin.")
    with col2:
        if st.button("Şifreyi Değiştir"):
            st.session_state.prev_page = st.session_state.page
            st.session_state.page = "Change Password"
            st.rerun()

# Hayvan ekle sayfası fonksiyonu
# TODO Bu sayfa da başka değişiklik yapılmayacaksa yeni .py dosyasına geçebilir
def add_animal_page():
    st.title("Hayvan Ekleme Ekrani")
    
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()

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
        st.rerun()
    st.write("Doktor ve Uygun Saatler Listesi")
    if st.button("Randevu Al"):
        # Placeholder for booking an appointment
        st.write("Randevu Al Buton")