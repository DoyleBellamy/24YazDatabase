
  <img src="https://github.com/user-attachments/assets/d120e779-6222-41e9-a983-6e6e49d606c0" alt="Görsel Açıklaması" width="300"/>


# Veteriner Klinik Yönetim Sistemi

Projemiz, bir Veteriner Kliniği için web tabanlı bir prototiptir. Sistem, üç farklı tipte kullanıcıya hizmet vermektedir: Hasta Hayvan Sahibi, Veteriner Hekim ve Admin. Her kullanıcı tipi, klinik operasyonlarına uygun olarak özelleştirilmiş işlevlere sahiptir.

### Sema Yapısı ve Veritabanı
**Semalar Klasörü:** Bu klasör, veri tabanı tasarımını gösteren EER (Entity-Relationship Diagram) ve İlişkisel Şema dosyalarını içerir. Bu belgeler, veri tabanındaki varlıklar ve bu varlıklar arasındaki ilişkiler hakkında kapsamlı bir genel bakış sağlar.

**SQL Codes Klasörü:** Bu klasörde, projede kullanılan tüm SQL komut dosyaları bulunur. Çalışmalar sırasında takım üyeleri arasında versiyon farklılıkları yaşanmaması için eski versiyonlar da klasörde tutulmuştur, ancak en güncel versiyonun kullanılması tavsiye edilir. Yerel bilgisayarınıza entegre edeceğiniz veri tabanını çalıştırmak için config dosyasını veri tabanınıza uygun niteliklerle (örneğin, şifre gibi) güncellemeyi unutmayın.

### Kullanıcı Tipleri ve İşlevler

**Hasta Hayvan Sahibi:**

- Hesabına hayvan bilgileri ekleyebilir ve bu bilgileri güncelleyebilir.
- İstediği hayvan için, istediği veterinerden uygun saatlere göre randevu alımı yapabilir.
- Geçmiş randevularının takibini yapabilir.
  
**Veteriner:**

- Aktif randevuları görüntüleyebilir.
- Randevu bazlı reçete yazabilir.
- Geçmiş randevuların takibini yapabilir.
- Bilgilerinde güncelleme yapabilir.
  
**Admin:**

- Sisteme yeni veteriner ve ilaç bilgileri girebilir.
- Gerektiğinde bu bilgileri sistemden kaldırabilir.

### Nasıl Çalıştırılır?

- Repository'İ lokal bilgisayarınıza kopyalayın:
  ```
  https://github.com/DoyleBellamy/24YazDatabase.git
  ```
- SQL Codes klasöründe bulunan güncel veri tabanı kodlarını kullandığınız MySQL destekli veri tabanı yönetim aracınızda çalıştırıp gerekli schemayı elde edin.
- config.py dosyasındaki bilgileri veri tabanınıza göre güncelleyin.
- Gerekli kütüphaneleri indirin:
  ```
  # Python ile MySQL veritabanı arasında bağlantı kurulmasını sağlar
  pip install mysql-connector-python
  # Python ile veri odaklı web uygulamaları geliştirilmesini kolaylaştırır
  pip install streamlit
  # Streamlit uygulamalarında etkileşimli ve dinamik veri tabloları oluşturmanızı sağlar
  pip install st-aggrid  
  ```
  
- app.py dosyasını çalıştırıp sizi web sayfasına yönlendirmesini bekleyin:
  ```
  streamlit run app.py
  ```
