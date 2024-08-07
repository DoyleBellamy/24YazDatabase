import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time, delete_data
from ilacEkleme import add_medicine_page
import GeneralUser as g
import randevu as r

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
    SELECT HastaID, İsim, Yaş, Boy, Kilo, Tür, Cinsiyet FROM bil372_project.hastahayvan
    WHERE SahipID = %s;
    """
    id_str = str(st.session_state.kullanıcı_id)
    animals_data = get_data(animal_query, (id_str,))

    if animals_data is not None and not animals_data.empty:
        st.write("Hayvanların Bilgileri:")

        if 'selected_animal_index' not in st.session_state:
            st.session_state.selected_animal_index = None

        for index, row in animals_data.iterrows():
            # Sütunları oluştur
            cols = st.columns([1, 6, 2, 1.2, 3])  
            
            with cols[0]:  # Checkbox sütunu
                if st.checkbox("", key=f"checkbox_{index}", value=(index == st.session_state.selected_animal_index)):
                    st.session_state.selected_animal_index = index
                    # Checkbox seçilince session_state'e hayvan_id ekle
                    st.session_state.hayvan_id = row["HastaID"]
                elif st.session_state.selected_animal_index == index:
                    st.session_state.selected_animal_index = None
            
            with cols[1]:  # Satır bilgisi sütunu
                # Her satır için küçük bir tablo oluşturma
                st.write(pd.DataFrame([row], columns=animals_data.columns))
            
            with cols[2]:  # Güncelle Butonu sütunu
                if st.button("Güncelle", key=f"update_{index}"):
                    st.session_state.selected_animal_id = row['HastaID']
                    st.session_state.prev_page = st.session_state.page
                    st.session_state.page = "update_animal"
                    st.experimental_rerun()
            
            with cols[3]:  # Sil Butonu sütunu
                delete_key = f"confirm_delete_{index}"

                if delete_key not in st.session_state:
                    st.session_state[delete_key] = False

                if st.button("Sil", key=f"button_{index}"):
                    st.session_state[delete_key] = not st.session_state[delete_key]

            # Eğer onay mesajı gösterilecekse
            if st.session_state[delete_key]:
                with cols[4]:
                    st.error("Silmek istediğine emin misin?")
                    yes_col, no_col = st.columns([1, 1.1])
                    with yes_col:
                        if st.button("Evet", key=f"yes_{index}"):
                            delete_query = "DELETE FROM bil372_project.hastahayvan WHERE HastaID = %s"
                            delete_data(delete_query, (row['HastaID'],))
                            st.session_state[delete_key] = False
                            st.experimental_rerun()
                    with no_col:
                        if st.button("Hayır", key=f"no_{index}"):
                            st.session_state[delete_key] = False
                            st.experimental_rerun()

        # Alt tarafta Randevu Al butonu
        if st.session_state.selected_animal_index is not None:
            selected_animal = animals_data.iloc[st.session_state.selected_animal_index]
            if st.button("Randevu Al"):
                st.session_state.prev_page = st.session_state.page
                st.session_state.page = "Book Appointment"
                st.session_state.selected_animal_id = selected_animal['HastaID']
                st.experimental_rerun()
        else:
            st.write("Randevu almak için bir hasta seçin.")

    col1, col2 = st.columns(2)
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
        email_adresi = st.text_input("E-Mail Adresi", value = email_adresi)
        
    with col2:
        ilce = st.text_input("İlce", value = ilce)
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
            st.session_state.page = "User Change Password"
            st.rerun()

def user_change_password_page():
    g.change_password_page(st.session_state.kullanıcı_id)
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.session_state.prev_page = "User Main"
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
    # Randevu için kullanıcı id ve hayvan id yi kullanarak hayvanın özelliklerini getir
    h_id = st.session_state.hayvan_id
    k_id = st.session_state.kullanıcı_id

    hayvan_query = """
    SELECT * FROM hastahayvan AS h WHERE h.HastaID = '{}' and h.SahipID = '{}'
    """.format(h_id,k_id)

    data1 = get_data(hayvan_query)

    # Hayvan türüne göre veterinerleri getir ve reviewlerine göre sırala
    vet_query = """
        With vet_puanları AS(
            SELECT v.KullanıcıID AS VetID,v.İsim AS Vetİsim, count(v.KullanıcıID) AS rew_sayısı  ,avg(r.puan) AS avg_p
            FROM veteriner AS v
            INNER JOIN reviewverir AS r
            ON v.KullanıcıID = r.VeterinerID
            group by(r.VeterinerID)
            order by avg_p desc
        )
        SELECT * 
        FROM yetkinlik AS y 
        INNER JOIN vet_puanları AS v 
        	ON v.VetID = y.VeterinerID 
        WHERE y.Yetkinlik = '{}'
        ORDER BY avg_p desc
    """.format(data1.iloc[0]["Tür"])

    data2 = get_data(vet_query)
    saatler = None

    # Sayfa görünümü
    st.title("Randevu Al")
    st.write("Veterinerler ve Uygun Saatler Listesi")
    if data2 is not None and not data2.empty:
        st.write("Veterinerler:")
        print(saatler)
        # Seçili satırları saklamak için bir liste
        selected_rows = []

        for index, row in data2.iterrows():

            vet_data = {
            "Veteriner İsmi": row["Vetİsim"],
            "Değerlendirme Sayısı": row["rew_sayısı"],
            "Puan": row["avg_p"]
            }

            # Sütunları oluştur
            cols = st.columns([1, 3, 1])  # 1: Checkbox için, 5: Satır Bilgisi için, 1: Buton için
            
            # Checkbox ve butonları ilgili sütunlara yerleştir
            with cols[0]:  # Checkbox sütunu
                checkbox = st.checkbox("", key=f"checkbox_{index}")
                if checkbox:    
                    selected_rows.append(index)
                    # Checkbox seçilince session_state'e hayvan_id ekle
                    st.session_state.veteriner_id = row["VeterinerID"]
                    if st.session_state.veteriner_id is not None:
                        saat_query = """
                        SELECT u.SaatID, u.VeterinerID FROM uygundur AS u 
                        INNER JOIN veteriner AS v ON v.KullanıcıID=u.VeterinerID 
                        INNER JOIN saatler AS s ON s.SaatID=u.SaatID
                        WHERE u.VeterinerID = '{}'
                        """.format(st.session_state.veteriner_id)
                        saatler = get_data(saat_query)
                        print(saatler)
                    
            with cols[1]:  # Satır bilgisi sütunu
                # Her satır için küçük bir tablo oluşturma
                st.write(pd.DataFrame([vet_data], columns=["Veteriner İsmi","Değerlendirme Sayısı","Puan"]))
    
    # Başlangıç ve bitiş tarihlerini kullanıcı seçer
    # Sistem bu tarihler arasında uygun en yakın tarih ve saatli randevuyu oluşturup kullanıcıya tanımlar
    st.write("Saat aralığı seçiniz")
    if(saatler is not None and not saatler.empty):
        cols2 = st.columns(2)
        with cols2[0]:

            start = st.date_input("Başlangıç:")
            print(start)
        with cols2[1]:

            end = st.date_input("Bitiş:")
            print(end)
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    
    if st.button("Randevu Al"):
        st.write("Randevu Al Buton")
        # Randevu returns a boolean 1 if successfull 0 if failure
        r.randevu(start,end)
        try:
            print("try")
            #r.randevu(start,end)
            #st.success("Randevu başarıyla alındı")
        except :
            print("except")
            #st.error("Randevu alınırken hata oluştu. Lütfen tekrar deneyiniz")

def update_animal_page():
    st.title("Hayvan Güncelleme Ekranı")
    
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()

    animal_id = st.session_state.selected_animal_id

    # Hayvanın mevcut bilgilerini getirme
    animal_query = "SELECT İsim, Yaş, Boy, Kilo, Tür, Cinsiyet FROM bil372_project.hastahayvan WHERE HastaID = %s"
    animal_data = get_data(animal_query, (animal_id,))

    if not animal_data.empty:
        animal = animal_data.iloc[0]
        hayvan_isim = st.text_input("İsim", value=animal['İsim'])
        hayvan_kilo = st.number_input("Kilo", min_value=0.0, step=0.1, value=float(animal['Kilo']))
        hayvan_boy = st.number_input("Boy", min_value=0.0, step=0.1, value=float(animal['Boy']))
        hayvan_yaş = st.number_input("Yaş", min_value=0.0, step=0.1, value=float(animal['Yaş']))
        hayvan_tur = st.selectbox("Tür", options=["Kedi", "Köpek", "Kuş", "Tavşan", "Kaplumbağa", "Hamster", "Kobay"], index=["Kedi", "Köpek", "Kuş", "Tavşan", "Kaplumbağa", "Hamster", "Kobay"].index(animal['Tür']))
        hayvan_cinsiyet = st.selectbox("Cinsiyet", options=["Dişi", "Erkek"], index=["Dişi", "Erkek"].index(animal['Cinsiyet']))
        
        # Güncelleme işlemi
        if st.button("Güncelle"):
            update_query = """
            UPDATE bil372_project.hastahayvan
            SET İsim = %s, Yaş = %s, Boy = %s, Kilo = %s, Tür = %s, Cinsiyet = %s
            WHERE HastaID = %s
            """
            params = (hayvan_isim, hayvan_yaş, hayvan_boy, hayvan_kilo, hayvan_tur, hayvan_cinsiyet, animal_id)
            update_data(update_query, params)
            st.write("Hayvan bilgileri güncellendi!")
    else:
        st.write("Hayvan bilgileri bulunamadı.")