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

1) Repository'i lokal bilgisayarına kopyalayın:
  ```
  https://github.com/DoyleBellamy/24YazDatabase.git
  ```
