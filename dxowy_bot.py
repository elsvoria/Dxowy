import sqlite3
import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# 🔧 Environment Variables Yükle
load_dotenv()

# 🔧 DXOWY BOT AYARLARI
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "YOUR_ADMIN_ID_HERE"))

# 🗂️ Veritabanı Ayarları
DB_FILE = "bot_orders.db"

# 🌍 DİL DESTEKLERİ
LANGUAGES = {
    'en': {
        'welcome': "🔥 **DXOWY'ye Hoş Geldiniz!**\n\nProfesyonel iş çözümleriniz için buradayız:\n• AI Otomasyon Sistemleri\n• Mobil Uygulama Geliştirme\n• Web Platform Tasarımı\n• Grafik & UI/UX Tasarım\n• Hızlı Proje Teslimi\n\n💼 **Hizmetlerimiz menüsünden** ihtiyacınıza uygun çözümü seçin!",
        'language_selected': "🎯 Language set to English! What would you like to do?",
        'services': "🛠️ **DXOWY Hizmetlerimiz**\n\n🤖 1. AI Otomasyon (Min. $500)\n📱 2. Mobil App Geliştirme (Min. $800)\n💻 3. Web Platform (Min. $600)\n🎨 4. Tasarım Hizmetleri (Min. $200)\n⚡ 5. FastTrack Projeler (Min. $300)\n\n💡 Hangi hizmeti tercih edersiniz?",
        'offer_system': "💰 OFFER SYSTEM\n\nPlease select which service you want to make an offer for:\n\n1️⃣ ⚡ FastTrack Development\n2️⃣ 🎨 Creative Design Solutions\n3️⃣ 🤖 AI Automation Systems\n4️⃣ 📱 Mobile App Development\n5️⃣ 🌐 Web Platform Creation\n\n📝 Reply with a number (1-5):",
        'service_selected': "✅ Service selected: {service}\n\n💵 Please enter your offer amount (in USD):",
        'offer_received': "🎉 Offer received!\n\n📋 Details:\n• Service: {service}\n• Amount: ${amount} USD\n• Your ID: {user_id}\n\n⏳ Our team will review your offer and get back to you within 24 hours.\n\n📞 For urgent matters: @dxowy_support",
        'offer_too_low': "💭 Thank you for your interest!\n\nHowever, for **{service}**, our starting price is **${min_price} USD** due to the complexity and quality standards we maintain.\n\n🎯 This service typically includes:\n• Professional development\n• Quality assurance\n• Post-delivery support\n• Documentation\n\n💡 Would you like to consider a budget closer to our starting range?",
        'offer_details_request': "✅ Great! Your budget of **${amount} USD** for **{service}** is within our range.\n\n📝 To provide you with an accurate quote, please share:\n\n🔹 **Project Details**: What exactly do you need?\n🔹 **Timeline**: When do you need it completed?\n🔹 **Specific Requirements**: Any special features or requirements?\n🔹 **Additional Notes**: Anything else we should know?\n\nPlease write all details in your next message.",
        'offer_summary': "📋 **PROJECT SUMMARY**\n\n👤 **Client**: {name}\n🛠️ **Service**: {service}\n💰 **Budget**: ${amount} USD\n📝 **Details**: {details}\n\n✅ **Please confirm all information is correct:**\n• YES → We'll send to our team\n• NO → You can make changes\n\nType 'YES' to confirm or 'NO' to modify.",
        'offer_confirmed': "🎉 **Project Successfully Submitted!**\n\nYour project has been sent to our development team. We'll review all details and provide you with:\n\n📄 **Detailed Quote**\n⏰ **Timeline & Milestones**\n💵 **Final Pricing**\n\nExpected response time: **24-48 hours**\n\n📞 Contact: @dxowy_support\n\nThank you for choosing DXOWY! 🚀",
        'contact_info': "📞 **Contact Information**\n\n✈️ **Telegram**: @dxowy_support\n📧 **Email**: contact@dxowy.com\n🌐 **Website**: www.dxowy.com\n📱 **WhatsApp**: +1 (555) 123-4567\n\n⏰ **Working Hours**: 24/7 Online\n🚀 **Response Time**: 2-4 hours\n\nOur team is excited to connect with you!",
        'about_info': "ℹ️ ABOUT DXOWY\n\n🏢 Company: DXOWY Technologies\n📅 Established: 2024\n🌍 Global Service Provider\n\n🎯 Our Mission:\nProviding innovative technology solutions worldwide with the highest quality standards.\n\n🔧 Specialties:\n• AI & Automation\n• Mobile Development\n• Web Solutions\n• Creative Design\n• Fast Development\n\n🏆 Why Choose DXOWY?\n✅ Professional Team\n✅ 24/7 Support\n✅ Quality Guarantee\n✅ Competitive Prices\n✅ Fast Delivery",
        'policy_info': "📋 DXOWY POLICY\n\n🔒 PRIVACY POLICY:\n• Your data is 100% secure\n• No sharing with third parties\n• GDPR compliant\n• Encrypted communications\n\n💰 PAYMENT POLICY:\n• Secure payment methods\n• 50% advance, 50% on delivery\n• Refund available if unsatisfied\n• Multiple payment options\n\n📝 SERVICE POLICY:\n• Written project agreements\n• Clear timelines and milestones\n• Regular progress updates\n• Post-delivery support included\n\n⚖️ TERMS OF SERVICE:\n• Professional conduct guaranteed\n• Intellectual property protection\n• Confidentiality agreements\n• Quality assurance standards\n\n📄 **Detailed Privacy Policy:**\n🔗 https://docs.google.com/document/d/1F6R6W_htN3LG2V_UorgXWLU1CJzb5-hCXBz0uOcu-A8/edit?usp=sharing",
        'buttons': {
            'services': '🛠️ Services',
            'offer': '💰 Make Offer',
            'contact': '📞 Contact',
            'about': 'ℹ️ About',
            'policy': '📋 Policy',
            'back': '🔙 Back'
        }
    },
    'tr': {
        'welcome': "🎉 DXOWY Bot'a Hoş Geldiniz! Merhaba {name} !\n\n✨ Devam etmek için dilinizi seçin:",
        'language_selected': "🎯 Dil Türkçe olarak ayarlandı! Ne yapmak istersiniz?",
        'services': "🛠️ DXOWY Hizmetleri\n\n💼 Mevcut Hizmetler:\n\n1️⃣ ⚡ Hızlı Geliştirme\n2️⃣ 🎨 Yaratıcı Tasarım Çözümleri\n3️⃣ 🤖 AI Otomasyon Sistemleri\n4️⃣ 📱 Mobil Uygulama Geliştirme\n5️⃣ 🌐 Web Platform Oluşturma\n\n💡 Bir hizmet seçin veya teklif verin!",
        'offer_system': "💰 TEKLİF SİSTEMİ\n\nLütfen hangi hizmet için teklif vermek istediğinizi seçin:\n\n1️⃣ ⚡ Hızlı Geliştirme\n2️⃣ 🎨 Yaratıcı Tasarım Çözümleri\n3️⃣ 🤖 AI Otomasyon Sistemleri\n4️⃣ 📱 Mobil Uygulama Geliştirme\n5️⃣ 🌐 Web Platform Oluşturma\n\n📝 Bir numara ile cevap verin (1-5):",
        'service_selected': "✅ Seçilen hizmet: {service}\n\n💵 Lütfen teklif miktarınızı girin (USD cinsinden):",
        'offer_received': "🎉 Teklif alındı!\n\n📋 Detaylar:\n• Hizmet: {service}\n• Miktar: ${amount} USD\n• Kullanıcı ID: {user_id}\n\n⏳ Ekibimiz teklifinizi inceleyecek ve 24 saat içinde geri dönüş yapacak.\n\n📞 Acil durumlar için: @dxowy_support",
        'offer_too_low': "💭 İlginiz için teşekkür ederiz!\n\nAncak **{service}** için başlangıç fiyatımız, sürdürdüğümüz karmaşıklık ve kalite standartları nedeniyle **${min_price} USD**'dir.\n\n🎯 Bu hizmet tipik olarak şunları içerir:\n• Profesyonel geliştirme\n• Kalite güvencesi\n• Teslimat sonrası destek\n• Dokümantasyon\n\n💡 Başlangıç aralığımıza daha yakın bir bütçe düşünmek ister misiniz?",
        'offer_details_request': "✅ Harika! **{service}** için **${amount} USD** bütçeniz aralığımız dahilinde.\n\n📝 Size doğru bir teklif sunabilmek için lütfen şunları paylaşın:\n\n🔹 **Proje Detayları**: Tam olarak neye ihtiyacınız var?\n🔹 **Zaman Çizelgesi**: Ne zaman tamamlanmasını istiyorsunuz?\n🔹 **Özel Gereksinimler**: Herhangi bir özel özellik veya gereksinim?\n🔹 **Ek Notlar**: Bilmemiz gereken başka bir şey?\n\nLütfen tüm detayları bir sonraki mesajınızda yazın.",
        'offer_summary': "📋 **PROJE ÖZETİ**\n\n👤 **Müşteri**: {name}\n🛠️ **Hizmet**: {service}\n💰 **Bütçe**: ${amount} USD\n📝 **Detaylar**: {details}\n\n✅ **Lütfen tüm bilgilerin doğru olduğunu onaylayın:**\n• EVET ise → Ekibimize göndereceğiz\n• HAYIR ise → Değişiklik yapabilirsiniz\n\nOnaylamak için 'EVET', değiştirmek için 'HAYIR' yazın.",
        'offer_confirmed': "🎉 **Proje Başarıyla Gönderildi!**\n\nProjeniz geliştirme ekibimize gönderildi. Tüm detayları inceleyip size şunları sunacağız:\n\n📄 **Detaylı Teklif**\n⏰ **Zaman Çizelgesi & Kilometre Taşları**\n💵 **Nihai Fiyat**\n\nBeklenen yanıt süresi: **24-48 saat**\n\n📞 İletişim: @dxowy_support\n\nDXOWY'yi seçtiğiniz için teşekkürler! 🚀",
        'contact_info': "📞 **İletişim Bilgileri**\n\n✈️ **Telegram**: @dxowy_support\n📧 **Email**: contact@dxowy.com\n🌐 **Website**: www.dxowy.com\n📱 **WhatsApp**: +1 (555) 123-4567\n\n⏰ **Çalışma Saatleri**: 7/24 Online\n🚀 **Yanıt Süresi**: 2-4 saat\n\nEkibimiz sizinle iletişime geçmek için sabırsızlanıyor!",
        'about_info': "ℹ️ DXOWY HAKKINDA\n\n🏢 Şirket: DXOWY Technologies\n📅 Kuruluş: 2024\n🌍 Global Hizmet Sağlayıcısı\n\n🎯 Misyonumuz:\nEn yüksek kalite standartlarıyla dünya çapında yenilikçi teknoloji çözümleri sunmak.\n\n🔧 Uzmanlık Alanları:\n• AI & Otomasyon\n• Mobil Geliştirme\n• Web Çözümleri\n• Yaratıcı Tasarım\n• Hızlı Geliştirme\n\n🏆 Neden DXOWY?\n✅ Profesyonel Ekip\n✅ 7/24 Destek\n✅ Kalite Garantisi\n✅ Rekabetçi Fiyatlar\n✅ Hızlı Teslimat",
        'policy_info': "📋 DXOWY POLİTİKA\n\n🔒 GİZLİLİK POLİTİKASI:\n• Verileriniz %100 güvenli\n• Üçüncü taraflarla paylaşım yok\n• GDPR uyumlu\n• Şifreli iletişim\n\n💰 ÖDEME POLİTİKASI:\n• Güvenli ödeme yöntemleri\n• %50 avans, %50 teslimde\n• Memnun değilseniz iade\n• Çoklu ödeme seçenekleri\n\n📝 HİZMET POLİTİKASI:\n• Yazılı proje sözleşmeleri\n• Net zaman çizelgeleri\n• Düzenli ilerleme raporları\n• Teslimat sonrası destek\n\n⚖️ HİZMET ŞARTLARI:\n• Profesyonel yaklaşım garantisi\n• Fikri mülkiyet koruması\n• Gizlilik anlaşmaları\n• Kalite güvence standartları\n\n📄 **Detaylı Gizlilik Politikası:**\n🔗 https://docs.google.com/document/d/1F6R6W_htN3LG2V_UorgXWLU1CJzb5-hCXBz0uOcu-A8/edit?usp=sharing",
        'buttons': {
            'services': '🛠️ Hizmetler',
            'offer': '💰 Teklif Ver',
            'contact': '📞 İletişim',
            'about': 'ℹ️ Hakkında',
            'policy': '📋 Politika',
            'back': '🔙 Geri'
        }
    },
    'de': {
        'welcome': "🎉 Willkommen bei DXOWY Bot! Hallo {name} !\n\n✨ Wählen Sie Ihre Sprache, um fortzufahren:",
        'language_selected': "🎯 Sprache auf Deutsch eingestellt! Was möchten Sie tun?",
        'services': "🛠️ DXOWY Dienstleistungen\n\n💼 Verfügbare Services:\n\n1️⃣ ⚡ Schnelle Entwicklung\n2️⃣ 🎨 Kreative Design-Lösungen\n3️⃣ 🤖 KI-Automatisierungssysteme\n4️⃣ 📱 Mobile App-Entwicklung\n5️⃣ 🌐 Web-Plattform-Erstellung\n\n💡 Wählen Sie einen Service oder machen Sie ein Angebot!",
        'offer_system': "💰 ANGEBOTSSYSTEM\n\nBitte wählen Sie, für welchen Service Sie ein Angebot machen möchten:\n\n1️⃣ ⚡ Schnelle Entwicklung\n2️⃣ 🎨 Kreative Design-Lösungen\n3️⃣ 🤖 KI-Automatisierungssysteme\n4️⃣ 📱 Mobile App-Entwicklung\n5️⃣ 🌐 Web-Plattform-Erstellung\n\n📝 Antworten Sie mit einer Zahl (1-5):",
        'service_selected': "✅ Service ausgewählt: {service}\n\n💵 Bitte geben Sie Ihren Angebotsbetrag ein (in USD):",
        'offer_received': "🎉 Angebot erhalten!\n\n📋 Details:\n• Service: {service}\n• Betrag: ${amount} USD\n• Ihre ID: {user_id}\n\n⏳ Unser Team wird Ihr Angebot prüfen und sich innerhalb von 24 Stunden bei Ihnen melden.\n\n📞 Für dringende Angelegenheiten: @dxowy_support",
        'offer_too_low': "💭 Vielen Dank für Ihr Interesse!\n\nFür **{service}** beträgt unser Startpreis jedoch **${min_price} USD** aufgrund der Komplexität und Qualitätsstandards.\n\n💡 Möchten Sie ein Budget näher an unserem Startbereich in Betracht ziehen?",
        'offer_details_request': "✅ Großartig! Ihr Budget von **${amount} USD** für **{service}** liegt in unserem Bereich.\n\n📝 Bitte teilen Sie Projektdetails mit.",
        'offer_summary': "📋 **PROJEKT ZUSAMMENFASSUNG**\n\n👤 **Kunde**: {name}\n🛠️ **Service**: {service}\n💰 **Budget**: ${amount} USD\n📝 **Details**: {details}\n\nAntworten Sie mit 'JA' zum Bestätigen.",
        'offer_confirmed': "🎉 **Projekt erfolgreich eingereicht!**\n\nErwartete Antwortzeit: **24-48 Stunden**\n\n📞 Kontakt: @dxowy_support",
        'contact_info': "📞 DXOWY KONTAKT\n\n🔗 Offizielle Kanäle:\n• Telegram: @dxowy_support\n• Support: 24/7 verfügbar\n• Antwortzeit: Innerhalb von 2 Stunden\n\n✅ Wir sind hier, um Ihnen zum Erfolg zu verhelfen!",
        'about_info': "ℹ️ ÜBER DXOWY\n\n🏢 Unternehmen: DXOWY Technologies\n📅 Gegründet: 2024\n🌍 Globaler Dienstleister\n\n🎯 Unsere Mission:\nInnovative Technologielösungen weltweit mit höchsten Qualitätsstandards anzubieten.\n\n🔧 Spezialisierungen:\n• KI & Automatisierung\n• Mobile Entwicklung\n• Web-Lösungen\n• Kreatives Design\n• Schnelle Entwicklung\n\n🏆 Warum DXOWY?\n✅ Professionelles Team\n✅ 24/7 Support\n✅ Qualitätsgarantie\n✅ Wettbewerbsfähige Preise\n✅ Schnelle Lieferung",
        'policy_info': "📋 DXOWY RICHTLINIE\n\n🔒 DATENSCHUTZRICHTLINIE:\n• Ihre Daten sind 100% sicher\n• Keine Weitergabe an Dritte\n• DSGVO-konform\n• Verschlüsselte Kommunikation\n\n💰 ZAHLUNGSRICHTLINIE:\n• Sichere Zahlungsmethoden\n• 50% Anzahlung, 50% bei Lieferung\n• Rückerstattung bei Unzufriedenheit\n• Mehrere Zahlungsoptionen\n\n📝 SERVICERICHTLINIE:\n• Schriftliche Projektverträge\n• Klare Zeitpläne und Meilensteine\n• Regelmäßige Fortschrittsupdates\n• Support nach Lieferung inklusive\n\n⚖️ NUTZUNGSBEDINGUNGEN:\n• Professionelles Verhalten garantiert\n• Schutz des geistigen Eigentums\n• Vertraulichkeitsvereinbarungen\n• Qualitätssicherungsstandards",
        'buttons': {
            'services': '🛠️ Services',
            'offer': '💰 Angebot machen',
            'contact': '📞 Kontakt',
            'about': 'ℹ️ Über uns',
            'policy': '📋 Richtlinie',
            'back': '🔙 Zurück'
        }
    },
    'ru': {
        'welcome': "🎉 Добро пожаловать в DXOWY Bot! Привет {name} !\n\n✨ Выберите ваш язык для продолжения:",
        'language_selected': "🎯 Язык установлен на русский! Что бы вы хотели сделать?",
        'services': "🛠️ Услуги DXOWY\n\n💼 Доступные услуги:\n\n1️⃣ ⚡ Быстрая разработка\n2️⃣ 🎨 Креативные дизайн-решения\n3️⃣ 🤖 Системы ИИ автоматизации\n4️⃣ 📱 Разработка мобильных приложений\n5️⃣ 🌐 Создание веб-платформ\n\n💡 Выберите услугу или сделайте предложение!",
        'offer_system': "💰 СИСТЕМА ПРЕДЛОЖЕНИЙ\n\nПожалуйста, выберите, для какой услуги вы хотите сделать предложение:\n\n1️⃣ ⚡ Быстрая разработка\n2️⃣ 🎨 Креативные дизайн-решения\n3️⃣ 🤖 Системы ИИ автоматизации\n4️⃣ 📱 Разработка мобильных приложений\n5️⃣ 🌐 Создание веб-платформ\n\n📝 Ответьте числом (1-5):",
        'service_selected': "✅ Выбрана услуга: {service}\n\n💵 Пожалуйста, введите сумму вашего предложения (в USD):",
        'offer_received': "🎉 Предложение получено!\n\n📋 Детали:\n• Услуга: {service}\n• Сумма: ${amount} USD\n• Ваш ID: {user_id}\n\n⏳ Наша команда рассмотрит ваше предложение и свяжется с вами в течение 24 часов.\n\n📞 По срочным вопросам: @dxowy_support",
        'contact_info': "📞 КОНТАКТ DXOWY\n\n🔗 Официальные каналы:\n• Telegram: @dxowy_support\n• Поддержка: Доступна 24/7\n• Время ответа: В течение 2 часов\n\n✅ Мы здесь, чтобы помочь вам добиться успеха!",
        'about_info': "ℹ️ О DXOWY\n\n🏢 Компания: DXOWY Technologies\n📅 Основана: 2024\n🌍 Глобальный поставщик услуг\n\n🎯 Наша миссия:\nПредоставление инновационных технологических решений по всему миру с высочайшими стандартами качества.\n\n🔧 Специализации:\n• ИИ и автоматизация\n• Мобильная разработка\n• Веб-решения\n• Креативный дизайн\n• Быстрая разработка\n\n🏆 Почему DXOWY?\n✅ Профессиональная команда\n✅ Поддержка 24/7\n✅ Гарантия качества\n✅ Конкурентные цены\n✅ Быстрая доставка",
        'policy_info': "📋 ПОЛИТИКА DXOWY\n\n🔒 ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ:\n• Ваши данные на 100% защищены\n• Не передаются третьим лицам\n• Соответствует GDPR\n• Зашифрованная связь\n\n💰 ПОЛИТИКА ОПЛАТЫ:\n• Безопасные способы оплаты\n• 50% аванс, 50% при доставке\n• Возврат при неудовлетворенности\n• Несколько вариантов оплаты\n\n📝 ПОЛИТИКА ОБСЛУЖИВАНИЯ:\n• Письменные договоры проекта\n• Четкие сроки и этапы\n• Регулярные обновления прогресса\n• Поддержка после доставки включена\n\n⚖️ УСЛОВИЯ ОБСЛУЖИВАНИЯ:\n• Гарантированное профессиональное поведение\n• Защита интеллектуальной собственности\n• Соглашения о конфиденциальности\n• Стандарты обеспечения качества",
        'buttons': {
            'services': '🛠️ Услуги',
            'offer': '💰 Сделать предложение',
            'contact': '📞 Контакт',
            'about': 'ℹ️ О нас',
            'policy': '📋 Политика',
            'back': '🔙 Назад'
        }
    },
    'es': {
        'welcome': "🎉 ¡Bienvenido a DXOWY Bot! ¡Hola {name} !\n\n✨ Elige tu idioma para continuar:",
        'language_selected': "🎯 ¡Idioma configurado en español! ¿Qué te gustaría hacer?",
        'services': "🛠️ Servicios DXOWY\n\n💼 Servicios disponibles:\n\n1️⃣ ⚡ Desarrollo rápido\n2️⃣ 🎨 Soluciones de diseño creativo\n3️⃣ 🤖 Sistemas de automatización IA\n4️⃣ 📱 Desarrollo de aplicaciones móviles\n5️⃣ 🌐 Creación de plataformas web\n\n💡 ¡Selecciona un servicio o haz una oferta!",
        'offer_system': "💰 SISTEMA DE OFERTAS\n\nPor favor, selecciona para qué servicio quieres hacer una oferta:\n\n1️⃣ ⚡ Desarrollo rápido\n2️⃣ 🎨 Soluciones de diseño creativo\n3️⃣ 🤖 Sistemas de automatización IA\n4️⃣ 📱 Desarrollo de aplicaciones móviles\n5️⃣ 🌐 Creación de plataformas web\n\n📝 Responde con un número (1-5):",
        'service_selected': "✅ Servicio seleccionado: {service}\n\n💵 Por favor, ingresa el monto de tu oferta (en USD):",
        'offer_received': "🎉 ¡Oferta recibida!\n\n📋 Detalles:\n• Servicio: {service}\n• Monto: ${amount} USD\n• Tu ID: {user_id}\n\n⏳ Nuestro equipo revisará tu oferta y se pondrá en contacto contigo en 24 horas.\n\n📞 Para asuntos urgentes: @dxowy_support",
        'contact_info': "📞 CONTACTO DXOWY\n\n🔗 Canales oficiales:\n• Telegram: @dxowy_support\n• Soporte: Disponible 24/7\n• Tiempo de respuesta: Dentro de 2 horas\n\n✅ ¡Estamos aquí para ayudarte a tener éxito!",
        'about_info': "ℹ️ ACERCA DE DXOWY\n\n🏢 Empresa: DXOWY Technologies\n📅 Establecida: 2024\n🌍 Proveedor de servicios global\n\n🎯 Nuestra misión:\nProporcionar soluciones tecnológicas innovadoras en todo el mundo con los más altos estándares de calidad.\n\n🔧 Especializaciones:\n• IA y automatización\n• Desarrollo móvil\n• Soluciones web\n• Diseño creativo\n• Desarrollo rápido\n\n🏆 ¿Por qué DXOWY?\n✅ Equipo profesional\n✅ Soporte 24/7\n✅ Garantía de calidad\n✅ Precios competitivos\n✅ Entrega rápida",
        'policy_info': "📋 POLÍTICA DXOWY\n\n🔒 POLÍTICA DE PRIVACIDAD:\n• Tus datos están 100% seguros\n• No se comparten con terceros\n• Cumple con GDPR\n• Comunicaciones encriptadas\n\n💰 POLÍTICA DE PAGO:\n• Métodos de pago seguros\n• 50% anticipo, 50% en entrega\n• Reembolso si no estás satisfecho\n• Múltiples opciones de pago\n\n📝 POLÍTICA DE SERVICIO:\n• Contratos de proyecto escritos\n• Cronogramas y hitos claros\n• Actualizaciones regulares de progreso\n• Soporte post-entrega incluido\n\n⚖️ TÉRMINOS DE SERVICIO:\n• Conducta profesional garantizada\n• Protección de propiedad intelectual\n• Acuerdos de confidencialidad\n• Estándares de aseguramiento de calidad",
        'buttons': {
            'services': '🛠️ Servicios',
            'offer': '💰 Hacer oferta',
            'contact': '📞 Contacto',
            'about': 'ℹ️ Acerca de',
            'policy': '📋 Política',
            'back': '🔙 Atrás'
        }
    }
}

# 🎯 Hizmetler ve Minimum Fiyatlar
SERVICES = {
    'en': {
        '1': '⚡ FastTrack Development',
        '2': '🎨 Creative Design Solutions',
        '3': '🤖 AI Automation Systems',
        '4': '📱 Mobile App Development',
        '5': '🌐 Web Platform Creation'
    },
    'tr': {
        '1': '⚡ Hızlı Geliştirme',
        '2': '🎨 Yaratıcı Tasarım Çözümleri',
        '3': '🤖 AI Otomasyon Sistemleri',
        '4': '📱 Mobil Uygulama Geliştirme',
        '5': '🌐 Web Platform Oluşturma'
    },
    'de': {
        '1': '⚡ Schnelle Entwicklung',
        '2': '🎨 Kreative Design-Lösungen',
        '3': '🤖 KI-Automatisierungssysteme',
        '4': '📱 Mobile App-Entwicklung',
        '5': '🌐 Web-Plattform-Erstellung'
    },
    'ru': {
        '1': '⚡ Быстрая разработка',
        '2': '🎨 Креативные дизайн-решения',
        '3': '🤖 Системы ИИ автоматизации',
        '4': '📱 Разработка мобильных приложений',
        '5': '🌐 Создание веб-платформ'
    },
    'es': {
        '1': '⚡ Desarrollo rápido',
        '2': '🎨 Soluciones de diseño creativo',
        '3': '🤖 Sistemas de automatización IA',
        '4': '📱 Desarrollo de aplicaciones móviles',
        '5': '🌐 Creación de plataformas web'
    }
}

# 💰 Minimum Fiyatlar (USD)
MINIMUM_PRICES = {
    '1': 300,  # Hızlı Geliştirme
    '2': 200,  # Tasarım
    '3': 500,  # AI Otomasyon
    '4': 800,  # Mobil App
    '5': 600   # Web Platform
}

# 📊 Kullanıcı Durumları
user_states = {}
user_languages = {}

# 🔧 Logging Ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def init_database():
    """🗂️ Veritabanını başlatır"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Kullanıcılar tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language TEXT DEFAULT 'tr',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Teklifler tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service_name TEXT,
            service_number TEXT,
            amount REAL,
            details TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Proje detayları tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            offer_id INTEGER,
            details TEXT,
            confirmed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (offer_id) REFERENCES offers (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_language(user_id):
    """👤 Kullanıcının dilini getirir"""
    if user_id in user_languages:
        return user_languages[user_id]
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        lang = result[0]
        user_languages[user_id] = lang
        return lang
    return 'en'  # Varsayılan dil

def save_user(user_id, username, first_name, language='tr'):
    """💾 Kullanıcıyı veritabanına kaydeder"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name, language)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, language))
    conn.commit()
    conn.close()
    user_languages[user_id] = language

def save_offer(user_id, service_name, service_number, amount):
    """💰 Teklifi veritabanına kaydeder"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO offers (user_id, service_name, service_number, amount)
        VALUES (?, ?, ?, ?)
    ''', (user_id, service_name, service_number, amount))
    offer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return offer_id

def save_project_details(user_id, offer_id, details):
    """📝 Proje detaylarını kaydeder"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO project_details (user_id, offer_id, details)
        VALUES (?, ?, ?)
    ''', (user_id, offer_id, details))
    conn.commit()
    conn.close()

def get_user_offer(user_id):
    """📋 Kullanıcının son teklifini getirir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, service_name, service_number, amount 
        FROM offers 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_main_keyboard(lang='tr'):
    """⌨️ Ana klavyeyi döndürür"""
    buttons = LANGUAGES[lang]['buttons']
    keyboard = [
        [buttons['services'], buttons['offer']],
        [buttons['contact'], buttons['about']],
        [buttons['policy']]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_language_keyboard():
    """🌍 Dil seçim klavyesini döndürür"""
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🚀 Start komutu"""
    user = update.effective_user
    user_id = user.id
    
    print(f"🎉 DXOWY BOT START! Kullanıcı: {user.first_name} (@{user.username}) - ID: {user_id}")
    
    # İngilizce karşılama mesajı
    welcome_text = f"🎉 Welcome to DXOWY Bot! Hello {user.first_name} !\n\n✨ Choose your language to continue:"
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_language_keyboard()
    )
    print("✅ DXOWY karşılama mesajı gönderildi!")
    
    # Admin'e bildirim gönder
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 DXOWY BOT: Yeni kullanıcı!\n👤 {user.first_name} (@{user.username})\n🆔 ID: {user_id}"
        )
    except Exception as e:
        print(f"⚠️ Admin bildirim hatası: {e}")

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🌍 Dil seçimi callback'i"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_id = user.id
    
    # Dil kodunu al
    lang_code = query.data.replace("lang_", "")
    
    # Kullanıcıyı kaydet
    save_user(user_id, user.username, user.first_name, lang_code)
    
    # Dil ayarlama mesajı
    lang_text = LANGUAGES[lang_code]['language_selected']
    
    # Sadece mesajı düzenle ve ana menüyü ekle
    await query.edit_message_text(
        text=lang_text,
        reply_markup=None
    )
    
    # Ana menüyü gönder (tekrar etmesin diye sadece klavyeyi gönder)
    await context.bot.send_message(
        chat_id=user_id,
        text="🎯 Menüyü kullanabilirsiniz:",
        reply_markup=get_main_keyboard(lang_code)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """📨 Mesaj işleyici"""
    user = update.effective_user
    message_text = update.message.text
    user_id = user.id
    
    # Kullanıcının dilini al
    lang = get_user_language(user_id)
    
    # Hizmetler
    if message_text == LANGUAGES[lang]['buttons']['services']:
        print("🛠️ DXOWY Services komutu çalıştı!")
        await update.message.reply_text(
            LANGUAGES[lang]['services'],
            reply_markup=get_main_keyboard(lang)
        )
    
    # Teklif ver
    elif message_text == LANGUAGES[lang]['buttons']['offer']:
        print("💰 DXOWY Offer komutu çalıştı!")
        user_states[user_id] = 'waiting_service_selection'
        await update.message.reply_text(
            LANGUAGES[lang]['offer_system'],
            reply_markup=ReplyKeyboardRemove()
        )
    
    # İletişim
    elif message_text == LANGUAGES[lang]['buttons']['contact']:
        await update.message.reply_text(
            LANGUAGES[lang]['contact_info'],
            reply_markup=get_main_keyboard(lang)
        )
    
    # Hakkında
    elif message_text == LANGUAGES[lang]['buttons']['about']:
        await update.message.reply_text(
            LANGUAGES[lang]['about_info'],
            reply_markup=get_main_keyboard(lang)
        )
    
    # Politika
    elif message_text == LANGUAGES[lang]['buttons']['policy']:
        await update.message.reply_text(
            LANGUAGES[lang]['policy_info'],
            reply_markup=get_main_keyboard(lang)
        )
    
    # Teklif sistemi - hizmet seçimi
    elif user_id in user_states and user_states[user_id] == 'waiting_service_selection':
        if message_text in ['1', '2', '3', '4', '5']:
            service_name = SERVICES[lang][message_text]
            user_states[user_id] = f'waiting_amount_{message_text}'
            await update.message.reply_text(
                LANGUAGES[lang]['service_selected'].format(service=service_name)
            )
        else:
            await update.message.reply_text(
                "❌ Lütfen 1-5 arasında bir sayı girin."
            )
    
    # Teklif sistemi - miktar girişi
    elif user_id in user_states and user_states[user_id] is not None and user_states[user_id].startswith('waiting_amount_'):
        try:
            amount = float(message_text)
            service_number = user_states[user_id].split('_')[2]
            service_name = SERVICES[lang][service_number]
            min_price = MINIMUM_PRICES[service_number]
            
            # Minimum fiyat kontrolü
            if amount < min_price:
                await update.message.reply_text(
                    LANGUAGES[lang]['offer_too_low'].format(
                        service=service_name,
                        min_price=min_price
                    ),
                    reply_markup=get_main_keyboard(lang)
                )
                # Durumu sıfırla
                user_states[user_id] = None
            else:
                # Makul fiyat - detay iste
                offer_id = save_offer(user_id, service_name, service_number, amount)
                user_states[user_id] = f'waiting_details_{offer_id}'
                
                await update.message.reply_text(
                    LANGUAGES[lang]['offer_details_request'].format(
                        amount=amount,
                        service=service_name
                    ),
                    reply_markup=ReplyKeyboardRemove()
                )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Lütfen geçerli bir sayı girin."
            )
    
    # Proje detayları bekleniyor
    elif user_id in user_states and user_states[user_id] is not None and user_states[user_id].startswith('waiting_details_'):
        offer_id = int(user_states[user_id].split('_')[2])
        details = message_text
        
        # Detayları kaydet
        save_project_details(user_id, offer_id, details)
        
        # Özet göster
        offer_data = get_user_offer(user_id)
        if offer_data:
            _, service_name, service_number, amount = offer_data
            
            summary_text = LANGUAGES[lang]['offer_summary'].format(
                name=user.first_name,
                service=service_name,
                amount=amount,
                details=details[:200] + "..." if len(details) > 200 else details
            )
            
            user_states[user_id] = f'waiting_confirmation_{offer_id}'
            
            await update.message.reply_text(
                summary_text,
                reply_markup=ReplyKeyboardRemove()
            )
    
    # Onay bekleniyor
    elif user_id in user_states and user_states[user_id] is not None and user_states[user_id].startswith('waiting_confirmation_'):
        if message_text.upper() in ['YES', 'EVET', 'JA', 'ДА', 'SÍ']:
            offer_id = int(user_states[user_id].split('_')[2])
            
            # Kullanıcıya onay mesajı
            await update.message.reply_text(
                LANGUAGES[lang]['offer_confirmed'],
                reply_markup=get_main_keyboard(lang)
            )
            
            # Admin'e detaylı bildirim gönder
            offer_data = get_user_offer(user_id)
            if offer_data:
                _, service_name, service_number, amount = offer_data
                
                # Proje detaylarını al
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute('SELECT details FROM project_details WHERE offer_id = ?', (offer_id,))
                details_result = cursor.fetchone()
                details = details_result[0] if details_result else "Detay bulunamadı"
                conn.close()
                
                admin_message = f"""� **YENİ PROJE TEKLİFİ**

👤 **Müşteri**: {user.first_name} (@{user.username})
🆔 **ID**: {user_id}
🛠️ **Hizmet**: {service_name}
� **Bütçe**: ${amount} USD
📝 **Proje Detayları**:
{details}

⚡ **AKSİYON GEREKLİ**
Bu teklifi değerlendirin ve müşteriye geri dönüş yapın."""

                try:
                    await context.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=admin_message
                    )
                except Exception as e:
                    print(f"⚠️ Admin bildirim hatası: {e}")
            
            # Durumu sıfırla
            user_states[user_id] = None
            
        elif message_text.upper() in ['NO', 'HAYIR', 'NEIN', 'НЕТ']:
            # Tekrar düzenleme imkanı
            await update.message.reply_text(
                "🔄 Tamam, tekrar başlayalım. 'Teklif Ver' butonuna basarak yeni bir teklif verebilirsiniz.",
                reply_markup=get_main_keyboard(lang)
            )
            user_states[user_id] = None
        else:
            await update.message.reply_text(
                "❓ Lütfen 'EVET' veya 'HAYIR' yazın."
            )
    
    # Dil seçimi (manuel)
    elif message_text.lower() in ['english', 'türkçe', 'deutsch', 'русский', 'español']:
        lang_map = {
            'english': 'en',
            'türkçe': 'tr', 
            'deutsch': 'de',
            'русский': 'ru',
            'español': 'es'
        }
        new_lang = lang_map[message_text.lower()]
        save_user(user_id, user.username, user.first_name, new_lang)
        
        await update.message.reply_text(
            LANGUAGES[new_lang]['language_selected'],
            reply_markup=get_main_keyboard(new_lang)
        )
    
    else:
        # Varsayılan yanıt
        await update.message.reply_text(
            "❓ Anlamadım. Lütfen menüden bir seçenek seçin.",
            reply_markup=get_main_keyboard(lang)
        )
    
    # Admin'e mesaj ilet
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📬 DXOWY MESAJ İLETİMİ\n\n👤 Gönderen: {user.first_name} (@{user.username})\n🆔 ID: {user_id}\n💬 Mesaj: {message_text}"
        )
    except Exception as e:
        print(f"⚠️ Admin mesaj iletme hatası: {e}")

def main():
    """🚀 Bot'u başlatır"""
    print("🚀 DXOWY BOT BAŞLATILIYOR...")
    print(f"🔑 DXOWY Token: {BOT_TOKEN[:10]}...")
    print(f"👨‍💻 Admin ID: {ADMIN_ID}")
    
    # Veritabanını başlat
    init_database()
    
    # Bot uygulamasını oluştur
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler'ları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 DXOWY Bot başlatıldı ve mesaj bekleniyor...")
    print("📱 Test için: @dxowybot'a git ve /start yaz")
    
    # Bot'u çalıştır (hızlı polling için)
    application.run_polling(poll_interval=1.0, timeout=20)

if __name__ == '__main__':
    main()
