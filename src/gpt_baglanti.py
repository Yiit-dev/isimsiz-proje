import json
import os
import time
import threading
import random

# Bu dosya önceden selenium için vardı şimdi gpt'yi tokenle kullancağımız için sildim yeni GUI kısmıyla entegra olan kısmı bıraktım

class GPTBaglanti:
    def __init__(self):
        self.oturum_acik = True
        self.aktif_sohbet_id = None
        self.sohbet_listesi = []
        self.sohbetler = {}
        self.mesajlar = {}
        self.ayarlari_yukle()
        
    def ayarlari_yukle(self):
        try:
            with open("ayarlar.json", "r", encoding="utf-8") as dosya:
                self.ayarlar = json.load(dosya)
        except Exception:
            self.ayarlari_olustur()
            
    def ayarlari_olustur(self):
        self.ayarlar = {
            "sistem": {
                "tema": "koyu",
                "varsayilan_mod": "normal",
                "ses_hizi": 150,
                "ses_volumu": 1.0,
                "mikrofon_hassasiyeti": 4000,
                "dil": "tr-TR",
                "pencere_genisligi": 1000,
                "pencere_yuksekligi": 600
            }
        }
        self.ayarlari_kaydet()
            
    def ayarlari_kaydet(self):
        try:
            with open("ayarlar.json", "w", encoding="utf-8") as dosya:
                json.dump(self.ayarlar, dosya, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ayarlar kaydedilemedi: {str(e)}")
    
    def sohbet_listesi_guncelle(self):
        return self.sohbet_listesi
    
    def sohbet_sec(self, sohbet_id):
        self.aktif_sohbet_id = sohbet_id
        return True
        
    def yeniSohbetBaslat(self):
        sohbet_id = f"sohbet_{int(time.time())}"
        baslik = f"Yeni Sohbet {len(self.sohbet_listesi) + 1}"
        
        self.sohbet_listesi.append({
            "id": sohbet_id,
            "baslik": baslik,
            "olusturma_zamani": time.time()
        })
        
        self.sohbetler[sohbet_id] = {"baslik": baslik}
        self.mesajlar[sohbet_id] = []
        self.aktif_sohbet_id = sohbet_id
        
        return sohbet_id
        
    def sohbet_sil(self, sohbet_id):
        if sohbet_id in self.sohbetler:
            del self.sohbetler[sohbet_id]
            
        if sohbet_id in self.mesajlar:
            del self.mesajlar[sohbet_id]
            
        self.sohbet_listesi = [s for s in self.sohbet_listesi if s["id"] != sohbet_id]
        
        if sohbet_id == self.aktif_sohbet_id:
            self.aktif_sohbet_id = self.sohbet_listesi[0]["id"] if self.sohbet_listesi else None
            
        return True
    
    def sohbet_yeniden_adlandir(self, sohbet_id, yeni_ad):
        if sohbet_id in self.sohbetler:
            self.sohbetler[sohbet_id]["baslik"] = yeni_ad
            
            for s in self.sohbet_listesi:
                if s["id"] == sohbet_id:
                    s["baslik"] = yeni_ad
                    break
                    
            return True
        return False
    
    def mesaj_gonder(self, mesaj):
        if not self.aktif_sohbet_id or self.aktif_sohbet_id not in self.mesajlar:
            return False
            
        self.mesajlar[self.aktif_sohbet_id].append({
            "metin": mesaj,
            "gonderen": "kullanici",
            "zaman": time.time()
        })
        
        return True
    
    def cevap_al(self):
        if not self.aktif_sohbet_id or self.aktif_sohbet_id not in self.mesajlar:
            return "Aktif sohbet bulunamadı."
            
        cevaplar = [
            "Merhaba! Size nasıl yardımcı olabilirim?",
            "Deneme123"
        ]
        
        yanit = random.choice(cevaplar)
        
        self.mesajlar[self.aktif_sohbet_id].append({
            "metin": yanit,
            "gonderen": "Yapay Zeka",
            "zaman": time.time()
        })
        
        return yanit
    
    def yanitAl(self, metin, detayli_dusunme=False, web_arama=False):
        self.mesaj_gonder(metin)
        
        if detayli_dusunme:
            time.sleep(3)
        else:
            time.sleep(1)
            
        return self.cevap_al()
    
    def get_sohbet_mesajlari(self, sohbet_id):
        return self.mesajlar.get(sohbet_id, []) 