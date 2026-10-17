# Task Manager Discord Bot

Küçük ekipler için görev yönetim botu. SQLite veritabanı ile çalışıyor. Görev ekleme, silme, listeleme ve tamamlama yapabiliyor. Tamamlanan görevler için Pollinations.ai API üzerinden kutlama görseli oluşturuyor.

## Reve API Hakkında

Projede Reve API ile görsel üretimi istenmiştir ancak Reve API şu anda yeni üye kabul etmemektedir. Bu yüzden alternatif olarak **Pollinations.ai** API kullandım. Çalışma mantığı Reve API ile birebir aynı:
- HTTP isteği ile prompt gönderiyorsun
- API sana üretilen görseli döndürüyor
- Ücretsiz ve API key gerektirmiyor

## Kurulum

1. Repoyu klonla:
   ```bash
   git clone <repo-url>
   cd task_manager_bot
   ```

2. Gerekli paketleri yükle:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` dosyası oluştur ve Discord token'ını ekle:
   ```
   DISCORD_TOKEN=buraya_kendi_tokenini_yaz
   ```

4. Botu çalıştır:
   ```bash
   python bot.py
   ```

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `!add_task <açıklama>` | Yeni görev ekler |
| `!show_tasks` | Tüm görevleri listeler |
| `!delete_task <id>` | Görevi siler |
| `!complete_task <id>` | Görevi tamamlandı olarak işaretler |
| `!celebrate <id>` | Tamamlanan görev için kutlama görseli oluşturur |

## Testler

```bash
pytest tests/ -v
```

ya da:

```bash
python run_tests.py
```

Testler in-memory SQLite kullanıyor yani asıl veritabanına dokunmuyor.

## Proje Yapısı

```
task_manager_bot/
├── bot.py                # ana bot dosyasi
├── database.py           # sqlite islemleri
├── image_generator.py    # gorsel uretimi (pollinations.ai api)
├── run_tests.py          # testleri calistirma scripti
├── requirements.txt
├── README.md
├── .env                  # discord token (git'e eklenmez)
├── .gitignore
├── images/               # uretilen gorseller
└── tests/
    ├── conftest.py
    ├── test_add_task.py
    ├── test_delete_task.py
    ├── test_show_task.py
    └── test_complete_task.py
```