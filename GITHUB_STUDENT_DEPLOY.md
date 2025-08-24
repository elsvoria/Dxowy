# 🎓 GitHub Student Pack + DigitalOcean Deploy Rehberi

## 1️⃣ **GitHub Student Pack Al**

### Adımlar:
1. [education.github.com/pack](https://education.github.com/pack) → Git
2. **"Get student benefits"** tıkla
3. **Öğrenci email** ile kayıt ol (.edu uzantılı)
4. **Öğrenci belgesi** yükle (transkript, kimlik)
5. **Onay bekle** (1-7 gün)

### 📧 **Öğrenci Email Yoksa:**
- Üniversitenden `.edu` email al
- Veya **öğrenci kimliği + transkript** yükle

## 2️⃣ **DigitalOcean Kredi Aktifleştir**

### GitHub Student Pack'ten:
1. **DigitalOcean** kartını bul
2. **"Get access"** tıkla  
3. **$200 kredi** otomatik eklenir
4. **2 yıl** geçerli

## 3️⃣ **DigitalOcean Droplet Oluştur**

### Droplet Ayarları:
- **Image:** Ubuntu 22.04 LTS
- **Plan:** Basic ($4/ay)
- **RAM:** 1GB (bot için yeterli)
- **CPU:** 1 vCPU
- **Storage:** 25GB SSD
- **Region:** Frankfurt (Türkiye'ye yakın)

## 4️⃣ **Bot Deploy Et**

### SSH ile Bağlan:
```bash
ssh root@DROPLET_IP
```

### Python & Bot Kurulumu:
```bash
# Python ve pip
apt update
apt install python3 python3-pip git -y

# Bot dosyalarını indir
git clone https://github.com/KULLANICI_ADI/dxowy-business-bot.git
cd dxowy-business-bot

# Paketleri yükle
pip3 install -r requirements.txt

# Environment variables ayarla
export TELEGRAM_TOKEN="8450361292:AAGKCuFzG2fCd6Mbceb7Ou1P5wx1Xg-udkA"
export ADMIN_ID="7562668997"

# Bot'u başlat
python3 dxowy_bot.py
```

## 5️⃣ **7/24 Çalıştır (systemd)**

### Service dosyası oluştur:
```bash
nano /etc/systemd/system/dxowy-bot.service
```

### İçerik:
```ini
[Unit]
Description=DXowy Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/dxowy-business-bot
ExecStart=/usr/bin/python3 dxowy_bot.py
Environment=TELEGRAM_TOKEN=8450361292:AAGKCuFzG2fCd6Mbceb7Ou1P5wx1Xg-udkA
Environment=ADMIN_ID=7562668997
Restart=always

[Install]
WantedBy=multi-user.target
```

### Service'i aktifleştir:
```bash
systemctl enable dxowy-bot
systemctl start dxowy-bot
systemctl status dxowy-bot
```

## 📊 **Maliyet Hesabı:**
- **$200 kredi** ÷ **$4/ay** = **50 ay**
- **4+ yıl** ücretsiz hosting
- **Sınırsız** çalışma

## 🎯 **Diğer Student Pack Bonusları:**
- **Heroku:** 1 yıl ücretsiz
- **Azure:** $100 kredi
- **AWS:** $100-200 kredi
- **MongoDB:** $200 kredi
- **Stripe:** İşlem ücreti muafiyeti

## 🔧 **Monitoring & Management:**
- DigitalOcean web paneli
- SSH ile terminal erişimi
- Real-time resource monitoring
- Automatic backups (opsiyonel)

## 💡 **Pro Tips:**
1. **Snapshot** al (backup için)
2. **Firewall** kuralları ayarla
3. **SSL sertifikası** ekle
4. **Domain** bağla (opsiyonel)
