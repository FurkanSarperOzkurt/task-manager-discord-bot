"""
Kutlama gorseli olusturucu modul.

Reve API yeni uye kabul etmedigi icin alternatif olarak
Pollinations.ai API kullaniyorum. 

Pollinations.ai ucretsiz ve API key gerektirmiyor.
"""

import requests
import os
import urllib.parse

# gorseller buraya kaydediyorum
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# pollinations api - reve api gibi calisiyor ama ucretsiz
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}?width=800&height=500&nologo=true"


def generate_celebration_image(task_description, task_id=None):
    """
    tamamlanan gorev icin kutlama gorseli olustur.
    pollinations api'ye prompt gonderip gorseli aliyorum.
    
    task_description: gorev aciklamasi
    task_id: dosya adi icin (opsiyonel)
    
    return: olusturulan gorselin dosya yolu
    """
    # images klasoru yoksa olustur
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # ingilizce prompt hazirliyorum cunku api ingilizce daha iyi calisiyor
    prompt = (
        f"A colorful celebration badge poster for completing a task: "
        f"{task_description}. Include confetti, stars, trophy icon, "
        f"bright colors, achievement style"
    )

    # url'ye koyacagim icin encode ediyorum
    encoded_prompt = urllib.parse.quote(prompt)
    url = POLLINATIONS_URL.format(prompt=encoded_prompt)

    # api'ye istek at
    resp = requests.get(url, timeout=60)

    if resp.status_code != 200:
        raise Exception(f"API hata dondurdu: HTTP {resp.status_code}")

    # gorseli kaydet
    filename = f"celebrate_{task_id or 'task'}.png"
    filepath = os.path.join(IMAGES_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(resp.content)

    return filepath
