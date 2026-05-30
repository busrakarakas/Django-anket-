"""
VoxPop - Demo Veri Yükleyici
BİLİŞİM SİSTEMLERİ öğrencileri için hazır anketler
"""
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'voxpop.settings'
django.setup()

from surveys.models import Category, Survey, Question, Choice

print("🧹 Eski veriler temizleniyor...")
Survey.objects.all().delete()
Category.objects.all().delete()

# ─── Kategoriler ───────────────────────────────────────────
cats = {
    'programlama': Category.objects.create(name='Programlama', slug='programlama', icon='💻', description='Diller, frameworks, araçlar'),
    'veritabani':  Category.objects.create(name='Veritabanı',  slug='veritabani',  icon='🗄️',  description='SQL, NoSQL, ORM'),
    'ag-guvenlik': Category.objects.create(name='Ağ & Güvenlik', slug='ag-guvenlik', icon='🔐', description='Siber güvenlik, ağ yönetimi'),
    'yazilim-eng': Category.objects.create(name='Yazılım Mühendisliği', slug='yazilim-eng', icon='⚙️', description='Metodolojiler, süreçler'),
    'kariyer':     Category.objects.create(name='Kariyer', slug='kariyer', icon='🚀', description='Meslek, sektör, hedefler'),
    'yapay-zeka':  Category.objects.create(name='Yapay Zeka', slug='yapay-zeka', icon='🤖', description='ML, AI araçları'),
    'bulut':       Category.objects.create(name='Bulut & DevOps', slug='bulut', icon='☁️', description='AWS, Azure, Docker'),
}

def survey_with_questions(title, desc, emoji, cat_key, is_featured, questions_data):
    s = Survey.objects.create(
        title=title, description=desc, thumbnail=emoji,
        category=cats[cat_key], survey_type='hazir',
        status='active', is_featured=is_featured
    )
    for i, (q_text, choices) in enumerate(questions_data, 1):
        q = Question.objects.create(survey=s, text=q_text, order=i)
        for j, (c_icon, c_text) in enumerate(choices, 1):
            Choice.objects.create(question=q, icon=c_icon, text=c_text, order=j)
    return s

# ═══════════════════════════════════════════════════════
# ANKET 1: Programlama Dilleri
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'En Popüler Programlama Dili 2024',
    'Bilişim öğrencilerinin ve yazılımcıların dil tercihleri ne yönde?',
    '💻', 'programlama', True,
    [
        ('Birincil programlama diliniz nedir?', [
            ('🐍','Python'), ('☕','Java'), ('⚡','JavaScript/TypeScript'),
            ('🦀','Rust'), ('🔷','C#/.NET'), ('🐹','Go'), ('⚙️','C/C++'), ('💎','Kotlin/Swift'),
        ]),
        ('Hangi alanda kod yazıyorsunuz?', [
            ('🌐','Web Geliştirme'), ('📱','Mobil Uygulama'),
            ('🤖','Yapay Zeka / Veri Bilimi'), ('⚙️','Backend / API'),
            ('🔐','Siber Güvenlik'), ('☁️','DevOps / Cloud'), ('🎮','Oyun Geliştirme'),
        ]),
        ('Yıllık deneyiminiz?', [
            ('🌱','Yeni başlıyorum (0-1 yıl)'), ('📗','1-3 yıl'),
            ('📘','3-5 yıl'), ('🏆','5+ yıl uzman'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 2: Veritabanı Tercihleri
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Veritabanı Tercihleri: SQL vs NoSQL',
    'Hangi veritabanı sistemlerini kullanıyorsunuz ve neden?',
    '🗄️', 'veritabani', True,
    [
        ('En çok kullandığınız veritabanı hangisi?', [
            ('🐘','PostgreSQL'), ('🐬','MySQL / MariaDB'), ('🗃️','SQLite'),
            ('🍃','MongoDB'), ('🔴','Redis'), ('☁️','Firebase'), ('📊','Microsoft SQL Server'),
        ]),
        ('SQL mi NoSQL mi tercih edersiniz?', [
            ('🟢','Her zaman SQL — yapılandırılmış veri şart'),
            ('🔵','Her zaman NoSQL — esneklik önemli'),
            ('⚖️','İkisi de — projeye göre değişir'),
            ('🤔','Henüz karar vermedim'),
        ]),
        ('ORM kullanıyor musunuz?', [
            ('✅','Evet, hep ORM kullanırım'), ('🔀','Bazen ORM bazen ham SQL'),
            ('❌','Hayır, direkt SQL yazarım'), ('🤷','ORM nedir bilmiyorum'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 3: Kariyer Hedefleri
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Bilişim Sistemleri Mezunlarının Kariyer Hedefleri',
    'Mezuniyet sonrası hangi kariyer yolunu hedefliyorsunuz?',
    '🚀', 'kariyer', True,
    [
        ('Mezun olduktan sonra hangi alanda çalışmak istiyorsunuz?', [
            ('💻','Yazılım Geliştirici / Mühendisi'), ('🔐','Siber Güvenlik Uzmanı'),
            ('📊','Veri Bilimci / Analist'), ('☁️','Cloud / DevOps Mühendisi'),
            ('🤖','Yapay Zeka / ML Mühendisi'), ('📱','Mobil Uygulama Geliştiricisi'),
            ('🏢','Sistem / Ağ Yöneticisi'), ('🧑‍💼','IT Proje Yöneticisi'),
        ]),
        ('Yurtiçi mi yurt dışı mı çalışmak istersiniz?', [
            ('🇹🇷','Türkiye\'de yerleşik'), ('🌍','Yurt dışında yaşamak istiyorum'),
            ('💻','Remote — ülke fark etmez'), ('🔀','Önce Türkiye, sonra göreceğiz'),
        ]),
        ('Kendi şirketinizi kurmayı düşünüyor musunuz?', [
            ('💡','Evet, girişimcilik hedefliyorum'), ('🤔','Belki ileride'),
            ('👔','Hayır, büyük şirkette çalışmayı tercih ederim'),
            ('🎓','Akademisyenlik / araştırma yapmak istiyorum'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 4: Siber Güvenlik
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Siber Güvenlik Farkındalık Anketi',
    'Bilişim güvenliği konusundaki alışkanlıklarınız ve bilginiz nasıl?',
    '🔐', 'ag-guvenlik', True,
    [
        ('Şifrelerinizi nasıl yönetiyorsunuz?', [
            ('🔑','Şifre yöneticisi kullanıyorum (1Password, Bitwarden...)'),
            ('🧠','Ezberliyor ve farklı şifreler kullanıyorum'),
            ('😬','Aynı şifreyi birden fazla yerde kullanıyorum'),
            ('📝','Bir yere not ediyorum'),
        ]),
        ('İki faktörlü kimlik doğrulama (2FA) kullanıyor musunuz?', [
            ('✅','Evet, her hesapta'), ('🔀','Önemli hesaplarda kullanıyorum'),
            ('❌','Hayır, kullanmıyorum'), ('🤷','2FA nedir bilmiyorum'),
        ]),
        ('En büyük siber tehdit olarak neyi görüyorsunuz?', [
            ('🎣','Phishing / Oltalama saldırıları'), ('🦠','Ransomware / Fidye yazılımı'),
            ('🕵️','Sosyal mühendislik'), ('💥','DDoS saldırıları'),
            ('🔓','Zayıf şifreler ve veri ihlalleri'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 5: Yapay Zeka Araçları
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Yapay Zeka Araçları Kullanım Anketi',
    'Günlük çalışma ve öğrenme sürecinizde AI araçlarını nasıl kullanıyorsunuz?',
    '🤖', 'yapay-zeka', True,
    [
        ('Hangi AI aracını en çok kullanıyorsunuz?', [
            ('🟢','ChatGPT'), ('🟣','Claude'), ('🔵','Google Gemini'),
            ('🟡','GitHub Copilot'), ('🦊','Perplexity'), ('❌','Kullanmıyorum'),
        ]),
        ('AI araçlarını nerede kullanıyorsunuz?', [
            ('💻','Kod yazmak / debug etmek için'), ('📚','Ders çalışmak / öğrenmek için'),
            ('✍️','Yazı / rapor hazırlamak için'), ('🔬','Araştırma yapmak için'),
            ('🎨','Görsel / içerik üretmek için'),
        ]),
        ('AI araçları eğitimi nasıl etkiliyor?', [
            ('📈','Öğrenmeyi kolaylaştırıyor, çok faydalı'),
            ('⚠️','Faydalı ama bağımlılık yaratıyor'),
            ('🤔','Emin değilim, iki yönlü etki var'),
            ('📉','Öğrencilerin düşünmesini engelliyor'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 6: Yazılım Geliştirme Metodolojileri
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Yazılım Geliştirme Metodolojileri',
    'Projelerde hangi metodolojileri ve araçları kullanıyorsunuz?',
    '⚙️', 'yazilim-eng', False,
    [
        ('Hangi metodoloji ile çalışıyorsunuz?', [
            ('🔄','Agile / Scrum'), ('🏃','Kanban'), ('📋','Waterfall'),
            ('🔀','Hybrid — duruma göre'), ('🤷','Henüz bilmiyorum'),
        ]),
        ('Versiyon kontrol sistemi kullanıyor musunuz?', [
            ('🐙','Evet, Git & GitHub / GitLab'),
            ('📁','Evet ama sadece dosya kopyalayarak'),
            ('❌','Hayır, kullanmıyorum'), ('🌱','Kullanmaya yeni başladım'),
        ]),
        ('Test yazıyor musunuz?', [
            ('✅','Evet, TDD uyguluyorum'), ('🔀','Bazen test yazıyorum'),
            ('❌','Hayır, hiç test yazmıyorum'), ('🤔','Test nedir biliyorum ama yazmıyorum'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 7: Bulut & DevOps
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Bulut ve DevOps Araçları Kullanımı',
    'Cloud platformları ve DevOps araçları hakkında ne kadar bilgi sahibisiniz?',
    '☁️', 'bulut', False,
    [
        ('Hangi cloud platformunu kullanıyorsunuz?', [
            ('🟠','AWS (Amazon)'), ('🔵','Azure (Microsoft)'), ('🟡','Google Cloud'),
            ('🔮','Heroku / Vercel / Netlify (basit deployment)'),
            ('❌','Henüz cloud kullanmıyorum'),
        ]),
        ('Docker kullanıyor musunuz?', [
            ('✅','Evet, aktif kullanıyorum'), ('📖','Öğrendim, az kullandım'),
            ('🌱','Şu an öğreniyorum'), ('❌','Bilmiyorum'),
        ]),
        ('CI/CD pipeline deneyiminiz var mı?', [
            ('🏭','Evet, kuruyorum ve yönetiyorum'), ('👀','Var olanı kullanıyorum'),
            ('📚','Kavramı biliyorum ama uygulamadım'), ('🤷','CI/CD nedir?'),
        ]),
    ]
)

# ═══════════════════════════════════════════════════════
# ANKET 8: Web Framework Tercihleri
# ═══════════════════════════════════════════════════════
survey_with_questions(
    'Web Geliştirme Framework Tercihleri',
    'Frontend ve backend tarafında hangi teknolojileri kullanmayı tercih ediyorsunuz?',
    '🌐', 'programlama', False,
    [
        ('Backend framework tercihiniz?', [
            ('🐍','Django (Python)'), ('⚡','FastAPI (Python)'), ('🟢','Node.js / Express'),
            ('🍀','Spring Boot (Java)'), ('💎','.NET / ASP.NET'), ('🔴','Laravel (PHP)'),
            ('🔵','NestJS'), ('🤷','Henüz bilmiyorum'),
        ]),
        ('Frontend tercihiniz?', [
            ('⚛️','React'), ('💚','Vue.js'), ('🔴','Angular'),
            ('🔺','Svelte'), ('⚡','Next.js / Nuxt.js'), ('🌿','Vanilla JS'),
        ]),
        ('Mobil geliştirme ilginizi çekiyor mu?', [
            ('📱','Evet, Native (Swift/Kotlin)'), ('🔀','React Native / Flutter tercih ederim'),
            ('💻','Hayır, web yeterli'), ('🤔','İkisine de ilgiliyim'),
        ]),
    ]
)

print(f"\n✅ Tüm hazır anketler oluşturuldu!")
print(f"   📋 {Survey.objects.count()} anket")
print(f"   ❓ {Question.objects.filter(survey__survey_type='hazir').count()} soru")
print(f"   🗳️ {Choice.objects.count()} seçenek")
print(f"   🏷️ {Category.objects.count()} kategori\n")

# Admin kullanıcısı
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@voxpop.com', 'admin123')
    print("👤 Admin hesabı oluşturuldu: admin / admin123")
else:
    print("👤 Admin zaten mevcut")

print("\n🚀 Sunucuyu başlatmak için: python manage.py runserver")
print("🌐 Adres: http://127.0.0.1:8000/")
print("⚙️  Admin: http://127.0.0.1:8000/admin/  →  admin / admin123")
