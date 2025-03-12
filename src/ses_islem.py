import threading
import queue
import time
import re
import os
import json

class SesKomutTanima:
    def __init__(self):
        self.dinleme_aktif = False
    
    def dinle(self):
        try:
            return "Bu bir test ses tanıma sistemidir."
        except Exception as e:
            return None

class SesKomut:
    def __init__(self):
        self.konusuyor = False
        self.konusma_kuyrugu = queue.Queue()
        self.ses_hizi = 150
        self.ses_volumu = 1.0
        self.ayarlari_yukle()
    
    def konus(self, metin):
        if not metin:
            return
            
        metin = self._metni_temizle(metin)
        
        try:
            self.konusuyor = True
            print(f"[SES ÇIKIŞ] {metin}")
            time.sleep(len(metin) * 0.05)
            self.konusuyor = False
        except Exception as e:
            print(f"Ses çıkışı hatası: {str(e)}")
            self.konusuyor = False

    def ayarlari_yukle(self):
        try:
            with open("ayarlar.json", "r", encoding="utf-8") as dosya:
                ayarlar = json.load(dosya)
                self.ses_hizi = ayarlar.get("sistem", {}).get("ses_hizi", 150)
                self.ses_volumu = ayarlar.get("sistem", {}).get("ses_volumu", 1.0)
        except Exception as e:
            print(f"Ses ayarları yüklenirken hata: {e}")
            self.ses_hizi = 150
            self.ses_volumu = 1.0
    
    def konusma_islemi(self):
        while True:
            try:
                metin = self.konusma_kuyrugu.get_nowait()
                self.konusuyor = True
                print(f"[SES ÇIKIŞ] {metin}")
                time.sleep(len(metin) * 0.05)
                self.konusuyor = False
            except queue.Empty:
                break
            except Exception as e:
                print(f"Konuşma hatası: {e}")
                self.konusuyor = False
                break
    
    def _metni_temizle(self, metin):
        if not metin:
            return ""
        temiz_metin = re.sub(r"http\S+|www.\S+", "", metin)
        temiz_metin = re.sub(r"[^\w\s\.,!?-]", "", temiz_metin)
        return temiz_metin.strip() 