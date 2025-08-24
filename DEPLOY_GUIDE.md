# 🚀 DXowy Bot - Railway Deploy Rehberi

## 📋 Adım Adım Deploy

### 1️⃣ **GitHub Repository Oluştur**
1. [GitHub.com](https://github.com) → "New Repository"
2. Repository adı: `dxowy-business-bot`
3. **Public** olarak oluştur
4. README.md ekle ✅

### 2️⃣ **Dosyaları GitHub'a Yükle**
VS Code Terminal'de:
```bash
cd dxowy_business_bot
git init
git add .
git commit -m "🚀 DXowy Bot initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADI/dxowy-business-bot.git
git push -u origin main
```

### 3️⃣ **Railway Hesabı Oluştur**
1. [Railway.app](https://railway.app) → "Sign up"
2. **GitHub ile giriş yap** (Önerilen)
3. Email doğrula ✅

### 4️⃣ **Railway'e Deploy**
1. Railway Dashboard → "**+ New Project**"
2. "**Deploy from GitHub repo**" seç
3. Repository'ni bul: `dxowy-business-bot`
4. **"Deploy Now"** tıkla
5. ⏳ Otomatik deploy başlar (2-3 dakika)

### 5️⃣ **Environment Variables Ayarla**
Railway project sayfasında:
1. **Variables** sekmesi → **"New Variable"**
2. 📝 Ekle:
   - **Name**: `TELEGRAM_TOKEN`
   - **Value**: `8450361292:AAGKCuFzG2fCd6Mbceb7Ou1P5wx1Xg-udkA`
3. 📝 İkinci variable:
   - **Name**: `ADMIN_ID` 
   - **Value**: `7562668997`
4. **"Add"** butonuna tıkla ✅

### 6️⃣ **Deploy Durumunu Kontrol Et**
1. **"Deployments"** sekmesi → Son deployment
2. **Yeşil ✅** görünce başarılı
3. **"View Logs"** ile detayları gör

## 🎉 **Deploy Tamamlandı!**

### ✅ **Artık Bot:**
- 🌍 **7/24 çalışıyor** (bulutta)
- 🔄 **Otomatik restart** yapıyor
- 📊 **Railway'de izlenebilir**
- 💡 **İnternetsiz çalışıyor**

### � **Test Et:**
1. Telegram'da @dxowybot'a git
2. `/start` komutu gönder
3. Bot yanıt veriyorsa ✅ başarılı!

## 🔄 **Bot Güncelleme**
Kod değiştirdikten sonra:
```bash
git add .
git commit -m "🔧 Bot güncellendi"
git push
```
Railway otomatik yeniden deploy eder! 🚀

## 📊 **Monitoring & Logs**
- **Railway Dashboard** → **Logs** sekmesi
- Gerçek zamanlı bot logları
- Hata durumunda anında bildirim
- CPU ve memory kullanımı

## 💰 **Maliyet Bilgisi**
Railway Ücretsiz Plan:
- ✅ **500 saat/ay** (20+ gün)
- ✅ **512MB RAM**
- ✅ **1 vCPU**
- ✅ **DXOWY Bot için yeterli**
- ✅ **Kredi kartı gerektirmez**

## 🔧 **Alternatif Platformlar**

### 🌐 **Render.com** (Backup seçenek)
- ✅ Ücretsiz
- ⚠️ 15 dakika boştaysa uyur
- 📝 Deploy: render.yaml gerekli

### ⚡ **Heroku** (Ücretli)
- ⚠️ $7/ay minimum
- ✅ Çok stabil
- ✅ Hiç uyumaz

## 🆘 **Sorun Giderme**

### ❌ Deploy başarısız ise:
1. **Logs** kontrol et
2. `requirements.txt` doğru mu?
3. `Procfile` var mı?
4. Environment variables eklenmiş mi?

### ❌ Bot yanıt vermiyorsa:
1. Railway Logs kontrol et
2. Token doğru mu?
3. Admin ID doğru mu?
4. Railway'de "Restart" dene

## 📞 **Destek**
- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- DXOWY Support: @dxowy_support
