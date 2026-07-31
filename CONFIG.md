# CONFIGURATION 
> Bu dosyadakik metin İngilizceye çevrilecek


Document to explain program's customization and configuration options.

### LISTEN_IP neden `0.0.0.0`?

Varsayılan olarak tüm ağ arayüzlerini dinler. Bunun iki sebebi var:
1. Oyun başka bir bilgisayarda çalışıyorsa, dashboard'ın o makineden gelen paketleri alabilmesi gerekir.
2. Windows'ta `127.0.0.1` (localhost) kullanıldığında, Windows Güvenlik Duvarı loopback UDP trafiğini engelleyebilir. `0.0.0.0` ile tüm arayüzler dinlendiğinde, oyunun `hardware_settings_config.xml` dosyasındaki `ip` adresini bilgisayarın yerel ağ IP'si (`192.168.x.x`) olarak ayarlamak yeterlidir — güvenlik duvarı bu trafiğe müdahale etmez.