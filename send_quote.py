import requests
import random
from translate import Translator
import time

# ----------- WHATSAPP AYARLARI (senin mevcut kodun) -----------
wh_url = "https://gate.whapi.cloud/messages/text"  # senin kullandığın URL
wh_token = "6uUr78Y77Dr1Bnn9RG2OXwRF4is9xVBM"
phone_number = "905432037091@s.whatsapp.net"

# ----------- PUSHBULLET AYARLARI -----------
PUSHBULLET_API_KEY = "o.jrPolPsG4D5eLRnKMdexgzWYaChbqJJS"  # buraya Pushbullet Access Token koy

# ----------- ALINTILAR -----------
quotes = [
    {"content": "Kod yazmak, bir dil öğrenmek gibidir. Her bir komut, evrende yeni bir anlam yaratır.", "author": "Bilinmiyor"},
    {"content": "Hataları anlamak, başarıya giden yoldur.", "author": "Edsger Dijkstra"},
    {"content": "Programcılar, sistemin ne yaptığıyla ilgilenirler. Yazılım geliştiricileri ise ne yapması gerektiğini anlam için çabalarlar.", "author": "Donald Knuth"},
    {"content": "İyi yazılım, sadece doğru çalışan yazılım değil, aynı zamanda sürdürülebilir ve bakımı kolay olan yazılımdır.", "author": "Kent Beck"},
    {"content": "Yazılım geliştirme, sanat ile mühendisliğin bir karışımıdır.", "author": "Bilinmiyor"},
    {"content": "Bir yazılımcı, bir problemi çözerken daha büyük bir problem yaratmamalıdır.", "author": "Bilinmiyor"},
    {"content": "Kod, yazıldığında bir amaca hizmet eder, ancak zamanla eskir ve yenilik gerektirir.", "author": "Martin Fowler"},
    {"content": "Her kod satırı bir fırsat, her hata ise bir öğrenme deneyimidir.", "author": "Bilinmiyor"},
    {"content": "Kodunuzu, bir başkası tarafından gece yarısı, acil bir şekilde debug yapması gerektiğini hayal ederek yazın.", "author": "John Woods"},
    {"content": "Yazılım geliştirme süreci, karmaşık düşüncelerin basit çözümlerle harmanlanmasıdır.", "author": "Bilinmiyor"},
 
]

def get_random_quote():
    q = random.choice(quotes)
    return f"{q['content']} -- {q['author']}"

def translate_to_tr(text):
    try:
        translator = Translator(to_lang="tr")
        return translator.translate(text)
    except Exception as e:
        print("Çeviri hatası, orijinal metin kullanılacak:", e)
        return text

def send_whatsapp_message(body_text):
    payload = {
        "typing_time": 5,
        "to": phone_number,
        "body": body_text,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    try:
        r = requests.post(f"{wh_url}?token={wh_token}", json=payload, headers=headers, timeout=15)
        print("WhatsApp yanıt kodu:", r.status_code)
        print("WhatsApp yanıt:", r.text)
        return r.status_code, r.text
    except Exception as e:
        print("WhatsApp gönderim hatası:", e)
        return None, str(e)

def send_pushbullet_notification(title, body):
    pb_url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "type": "note",
        "title": title,
        "body": body
    }
    try:
        r = requests.post(pb_url, json=data, headers=headers, timeout=10)
        print("Pushbullet yanıt kodu:", r.status_code)
        # r.json() içeriğini yazdırma (isteğe bağlı)
        return r.status_code, r.text
    except Exception as e:
        print("Pushbullet hatası:", e)
        return None, str(e)

if __name__ == "__main__":
    quote = get_random_quote()
    translated = translate_to_tr(quote)

    # 1) WhatsApp gönder (orijinal akış)
    print("WhatsApp'a gönderiliyor...")
    wh_status, wh_resp = send_whatsapp_message(translated)

    # 2) Pushbullet ile telefonunda bildirim göster
    print("Pushbullet bildirimi gönderiliyor...")
    title = "Programlama Alıntısı"
    pb_status, pb_resp = send_pushbullet_notification(title, translated)

    # Durum özetleri
    print("Özet:")
    print("WhatsApp:", wh_status)
    print("Pushbullet:", pb_status)
