import streamlit as st
import mysql.connector
import pandas as pd
import re
from utils import get_data, update_data, get_highest_id, insert_data, format_time, delete_data
from ilacEkleme import add_medicine_page
import GeneralUser as g
import datetime as d
import randevu as r
from st_aggrid import AgGrid, GridOptionsBuilder

# Kullanıcı ana sayfa fonksiyonu
# İçindeki sayfalar:
#   - user_main_page 
#   - past_appointments_page
#   - user_info_page
#   - add_animal_page
#   - book_appointment_page

st.session_state.btn = None
def user_main_page():
    st.title("Kullanıcı Ana Sayfa")
    st.write("Hayvanlar Listesi ve Bilgileri ve Randevu Alma")

    # Kullanıcının hayvanlarını getir
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
                    st.rerun()
            
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
                            st.rerun()
                    with no_col:
                        if st.button("Hayır", key=f"no_{index}"):
                            st.session_state[delete_key] = False
                            st.rerun()

        # Alt tarafta Randevu Al butonu
        now = d.date.today()
        q = """
        select Tarih
        from randevu
        where SahipID ='{}' and Tarih between '{}' and '{}'
        limit 1
        ;
        """.format(st.session_state.kullanıcı_id,now - d.timedelta(days=7),now)

        randevular = get_data(q)
        if st.session_state.selected_animal_index is not None:
            selected_animal = animals_data.iloc[st.session_state.selected_animal_index]
            if st.button("Randevu Al"):
                if randevular.empty:
                    st.session_state.prev_page = st.session_state.page
                    st.session_state.page = "Book Appointment"
                    st.session_state.selected_animal_id = selected_animal['HastaID']
                    st.rerun()
                else:
                    st.error("Son 7 gün içerisinde randevunuz bulunmaktadır. Randevu alınamaz")
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
    
    q ="""
    select r.VeterinerID,v.isim as 'Veteriner İsmi',r.HastaID, r.Tarih
    from randevu as r
    inner join veteriner as v
	    on v.KullanıcıID = r.VeterinerID
    where r.Tarih<'{}' and r.SahipID = '{}'
    ;
    """.format(d.date.today(),st.session_state.kullanıcı_id)

    try:
        randevular = get_data(q)
    except:
        st.error("Geçmiş randevular getirilirken bir hata oluştu. Lütfen tekrar deneyiniz.")
    selected_rows = pd.DataFrame()

    st.title("Geçmiş Randevular")
    
    if randevular is not None and not randevular.empty:
        # Convert data to a DataFrame
        df = pd.DataFrame(randevular)
        
    
        # Create a GridOptionsBuilder instance
        gb = GridOptionsBuilder.from_dataframe(df)
        # Configure selection and layout options
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
        
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

    
    col1, col2 = st.columns(2)
    if selected_rows is not None and not selected_rows.empty:
            print("VetID:")
            print(selected_rows['VeterinerID'][0])
            st.session_state.veteriner_id = selected_rows['VeterinerID'][0]
            print("HastaID:")
            print(selected_rows['HastaID'][0])
            st.session_state.hayvan_id = selected_rows['HastaID'][0]

            with col1:
                if st.button("Veterineri Değerlendir"):
                    st.session_state.btn = 1
                    #Review bilgileri

                
            with col2:
                if st.button("Reçete"):
                    st.session_state.btn = 2
                    

    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    if "btn" in st.session_state:
        match st.session_state.btn:
            case 1:
                #Review bilgileri

                #Önceden review var mı kontrol et
                rev_q="""
                select * 
                from reviewverir 
                where HayvanSahibiID='{}' and VeterinerID='{}'   
                """.format(st.session_state.kullanıcı_id,st.session_state.veteriner_id)
                rev_d = get_data(rev_q)
                print(rev_d)
                aciklama=""
                puan = 0
                anon = False
                if rev_d is not None and not rev_d.empty:
                    aciklama=rev_d.iloc[0]['Açıklama']
                    puan = rev_d.iloc[0]['Puan']
                    # 0 ise anonim, 1 ise anonim değil
                    anon = rev_d.iloc[0]['Anonim']

                container = st.container(border=True)

                container.title("Veteriner Değerlendir")
            
                container.info("Değerlendirmenizin başka kullanıcılar tarafından görülmesini istemiyorsanız aşağıdaki kutuyu işaretleyiniz.")
                anon = container.checkbox("Anonim",value=anon)
            
                aciklama = container.text_area("Değerlendirmenizi yazınız:",value=aciklama,max_chars=250)
            
                puan = container.number_input("Veteriner Puanı:",value=puan,min_value=0,max_value=10)

                if rev_d is not None and not rev_d.empty:
                    if container.button("Düzenle"):
                        update_q = """
                        UPDATE reviewverir SET Açıklama = %s, Puan = %s, Anonim = %s WHERE HayvanSahibiID = %s and VeterinerID = %s
                        """
                        params = aciklama,str(puan),anon,str(st.session_state.kullanıcı_id),str(st.session_state.veteriner_id)
                        try:
                            update_data(update_q,params)
                            container.success("Değerlendirmeniz başarıyla düzenlendi.")
                        except:
                            container.error("Değerlendirme düzenlenirken bir hata oluştu. Lütfen tekrar deneyiniz")
                else:
                    if container.button("Gönder"):
                        insert_q = """
                        insert into reviewverir values(%s,%s,%s,%s,%s)
                        """
                        p = str(st.session_state.kullanıcı_id),str(st.session_state.veteriner_id),aciklama,str(puan),anon
                        try:
                            insert_data(insert_q,p)
                            container.success("Değerlendirmeniz başarıyla gönderildi.")
                        except:
                            container.error("Değerlendirme gönderilirken bir hata oluştu. Lütfen tekrar deneyiniz")
                        
            
            case 2:
                # Reçete bilgileri
                if randevular is not None and not randevular.empty:
                    print(randevular.iloc[0]['Tarih'])
                    print(randevular.iloc[0]['Tarih']+d.timedelta(days=1))
                    r_q ="""
                    select e.ReçeteID, e.Tarih, e.aciklama as 'Açıklama'
                    from randevu as r
                    inner join reçete as e
	                on e.VeterinerID = r.VeterinerID and e.HastaHayvanID = r.HastaID
                    where r.VeterinerID ='{}' and r.SahipID ='{}' and r.HastaID = '{}' and e.Tarih between r.Tarih and Date_ADD(r.Tarih, INTERVAL +1 day)
                    """.format(st.session_state.veteriner_id,st.session_state.kullanıcı_id,st.session_state.hayvan_id)
                    d_r = get_data(r_q)
                    print(d_r)

                    selected_rows_recete = pd.DataFrame()
    
                    if d_r is not None and not d_r.empty:
                        # Convert data to a DataFrame
                        df = pd.DataFrame(d_r)
        
    
                        # Create a GridOptionsBuilder instance
                        gb = GridOptionsBuilder.from_dataframe(df)
                        # Configure selection and layout options
                        gb.configure_selection('single')
        
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

                        selected_rows_recete = grid_response['selected_rows']

    

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
            SELECT v.KullanıcıID AS VetID,v.İsim AS `Veteriner ismi`, count(v.KullanıcıID) AS `Değerlendirme Sayısı`  ,avg(r.puan) AS `Puan`
            FROM veteriner AS v
            INNER JOIN reviewverir AS r
            ON v.KullanıcıID = r.VeterinerID
            group by(r.VeterinerID)
            order by 'Puan' desc
        )
        SELECT v.VetID,v.`Veteriner ismi`, v.`Değerlendirme Sayısı`, v.`Puan`
        FROM yetkinlik AS y 
        INNER JOIN vet_puanları AS v 
        	ON v.VetID = y.VeterinerID 
        WHERE y.Yetkinlik = '{}'
        ORDER BY `Puan` desc
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
        # Convert data to a DataFrame
        df = pd.DataFrame(data2)
        
    
        # Create a GridOptionsBuilder instance
        gb = GridOptionsBuilder.from_dataframe(df)
        # Configure selection and layout options
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
        
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

        if selected_rows is not None and not selected_rows.empty:
            print("VetID:")
            print(selected_rows['VetID'][0])
            st.session_state.veteriner_id = selected_rows['VetID'][0]
        
    
    # Başlangıç ve bitiş tarihlerini kullanıcı seçer
    # Sistem bu tarihler arasında uygun en yakın tarih ve saatli randevuyu oluşturup kullanıcıya tanımlar
    st.write("Tarih aralığı seçiniz")
    cols2 = st.columns(2)
    with cols2[0]:
        start = st.date_input("Başlangıç:")
        print(start)

    with cols2[1]:
            end = st.date_input("Bitiş:")
            print(end)

    #if(saatler is not None and not saatler.empty):
        
    if st.button("Geri"):
        st.session_state.page = st.session_state.prev_page
        st.rerun()
    

    #print(randevular.empty)
    if st.button("Randevu Al") :
        if start>=d.date.today() :
            if(start<=end):
                r.randevu(start,end)
            else:
                st.error("Bitiş tarihi başlangıç tarihinden önce olamaz. Tarihleri düzenleyip tekrar deneyiniz")
        else:
            st.error("Geçmiş tarihli randevu alınamaz")


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

