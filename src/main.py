import sys
import threading
import os
import time
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QScrollArea, QLabel, QFrame, QSizePolicy, QGraphicsOpacityEffect, QMessageBox, QSplitter, QSplashScreen, QToolButton, QMenu, QButtonGroup, QCheckBox, QSlider, QFileDialog, QDialog, QRadioButton
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRect, QParallelAnimationGroup, QEvent, QSequentialAnimationGroup, QSettings
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette, QPixmap, QPainter, QBrush, QPen, QLinearGradient, QImage, QFontDatabase, QAction, QKeySequence, QShortcut, QCursor, QPainterPath

from src.gpt_baglanti import GPTBaglanti
from src.ses_islem import SesKomutTanima, SesKomut
from src.model_gorunum import ModelGorunum3D
from src.sohbet_yonetici import SohbetYonetici

class TemaYoneticisi:
    def __init__(self):
        self.ayarlar = QSettings("AiChatApp", "TemaAyarlari")
        self.temalar = {
            "acik": {
                "arkaplan": "#FFFFFF",
                "panel": "#FFFFFF",
                "panel_sekonder": "#F8F8F8",
                "buton": "#F5F5F5",
                "buton_hover": "#E8E8E8",
                "buton_aktif": "#0078D4",
                "vurgu": "#0078D4",
                "metin": "#000000",
                "metin_ikincil": "#444444",
                "kenar": "#E0E0E0",
                "hata": "#D83B01",
                "basari": "#107C10",
                "kullanici_mesaj": "#E7F5FF",
                "yapay_zeka_mesaj": "#F8F8F8",
                "golge": "rgba(0, 0, 0, 0.05)"
            },
            "koyu": {
                "arkaplan": "#121212",
                "panel": "#1E1E1E",
                "panel_sekonder": "#252525",
                "buton": "#2D2D2D",
                "buton_hover": "#3E3E3E",
                "buton_aktif": "#60CDFF",
                "vurgu": "#60CDFF",
                "metin": "#FFFFFF",
                "metin_ikincil": "#AAAAAA",
                "kenar": "#333333",
                "hata": "#F85858",
                "basari": "#6CCB5F",
                "kullanici_mesaj": "#1F2B3E",
                "yapay_zeka_mesaj": "#252525",
                "golge": "rgba(0, 0, 0, 0.3)"
            }
        }
        
        try:
            with open("ayarlar.json", "r", encoding="utf-8") as f:
                ayarlar = json.load(f)
                varsayilan_tema = ayarlar.get("sistem", {}).get("tema", "koyu")
                self.aktif_tema = self.ayarlar.value("tema", varsayilan_tema)
        except Exception:
            self.aktif_tema = "koyu"
        
    def tema_degistir(self, tema_adi):
        if tema_adi in self.temalar:
            self.aktif_tema = tema_adi
            self.ayarlar.setValue("tema", tema_adi)
            return True
        return False
    
    def renkleri_al(self):
        return self.temalar[self.aktif_tema]
    
    def css_degiskenler(self):
        renkler = self.renkleri_al()
        css = f"""
            * {{
                font-family: 'Segoe UI', sans-serif;
            }}
            
            #AnaForm {{
                background-color: {renkler['arkaplan']};
                color: {renkler['metin']};
            }}
            
            QWidget {{
                background-color: transparent;
                color: {renkler['metin']};
            }}
            
            QFrame#icerikAlani {{
                background-color: {renkler['panel']};
                border-radius: 12px;
                border: 1px solid {renkler['kenar']};
            }}
            
            QLineEdit, QTextEdit {{
                background-color: {renkler['panel_sekonder']};
                color: {renkler['metin']};
                border: 1px solid {renkler['kenar']};
                border-radius: 8px;
                padding: 8px;
                selection-background-color: {renkler['vurgu']};
                selection-color: white;
            }}
            
            QPushButton {{
                background-color: {renkler['buton']};
                color: {renkler['metin']};
                border: 1px solid {renkler['kenar']};
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background-color: {renkler['buton_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {renkler['vurgu']};
                color: white;
            }}
            
            QPushButton:checked {{
                background-color: {renkler['vurgu']};
                color: white;
                font-weight: bold;
            }}
            
            QToolButton {{
                background-color: {renkler['buton']};
                border: 1px solid {renkler['kenar']};
                border-radius: 8px;
                padding: 3px;
            }}
            
            QToolButton:hover {{
                background-color: {renkler['buton_hover']};
            }}
            
            QToolButton:pressed {{
                background-color: {renkler['vurgu']};
            }}
            
            QScrollArea, QScrollBar {{
                background-color: transparent;
                border: none;
            }}
            
            QScrollBar:vertical {{
                background-color: transparent;
                width: 14px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {renkler['buton']};
                min-height: 20px;
                border-radius: 7px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {renkler['buton_hover']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background-color: transparent;
                height: 0px;
                width: 0px;
            }}
            
            QMenu {{
                background-color: {renkler['panel']};
                border: 1px solid {renkler['kenar']};
                border-radius: 8px;
                padding: 5px;
            }}
            
            QMenu::item {{
                background-color: transparent;
                padding: 6px 25px 6px 20px;
                border-radius: 4px;
                margin: 2px;
            }}
            
            QMenu::item:selected {{
                background-color: {renkler['buton_hover']};
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {renkler['kenar']};
                margin: 5px 10px;
            }}
            
            QLabel {{
                color: {renkler['metin']};
            }}
            
            QMessageBox {{
                background-color: {renkler['panel']};
            }}
            
            QMessageBox QPushButton {{
                min-width: 80px;
                min-height: 30px;
            }}
            
            QSplitter::handle {{
                background-color: {renkler['kenar']};
            }}
            
            QSplitter::handle:horizontal {{
                width: 1px;
            }}
            
            QSplitter::handle:vertical {{
                height: 1px;
            }}
            
            QToolTip {{
                background-color: {renkler['panel']};
                color: {renkler['metin']};
                border: 1px solid {renkler['kenar']};
                border-radius: 4px;
                padding: 5px;
            }}
        """
        return css

class MesajKarti(QFrame):
    def __init__(self, metin, gonderici="kullanici", parent=None, tema_yonetici=None):
        super().__init__(parent)
        self.metin = metin
        self.gonderici = gonderici
        self.tema_yonetici = tema_yonetici
        
        self.setMaximumWidth(600)
        self.setMinimumWidth(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        
        self.kurulum()
        self.animasyonBaslat()
        
    def animasyonBaslat(self):
        self.anim_grup = QParallelAnimationGroup(self)
        
        opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        opacity_anim.setDuration(200)
        opacity_anim.setStartValue(0)
        opacity_anim.setEndValue(1)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        slide_anim = QPropertyAnimation(self, b"geometry", self)
        slide_anim.setDuration(200)
        baslangic_geo = self.geometry()
        baslangic_geo.setY(int(baslangic_geo.y() + 20))
        
        slide_anim.setStartValue(baslangic_geo)
        slide_anim.setEndValue(self.geometry())
        slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.anim_grup.addAnimation(opacity_anim)
        self.anim_grup.addAnimation(slide_anim)
        self.anim_grup.start()
    
    def kurulum(self):
        renkler = self.tema_yonetici.renkleri_al() if self.tema_yonetici else {
            "kullanici_mesaj": "#E9F2FF",
            "yapay_zeka_mesaj": "#F5F5F9",
            "vurgu": "#0078D4",
            "metin": "#202020",
            "metin_ikincil": "#5D5D5D",
            "kenar": "#E6E6E6",
            "golge": "rgba(0, 0, 0, 0.08)"
        }
        
        duzen = QVBoxLayout(self)
        duzen.setContentsMargins(16, 16, 16, 16)
        duzen.setSpacing(8)
        
        ust_duzen = QHBoxLayout()
        ust_duzen.setSpacing(10)
        
        profil_widget = QFrame(self)
        profil_widget.setFixedSize(36, 36)
        profil_widget.setObjectName("profilWidget")
        
        profil_duzen = QVBoxLayout(profil_widget)
        profil_duzen.setContentsMargins(0, 0, 0, 0)
        
        profil_ikon = QLabel(profil_widget)
        profil_ikon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profil_ikon.setFixedSize(36, 36)
        
        if self.gonderici == "kullanici":
            profil_pixmap = QPixmap("src/model/kullanici_ikon.png")
            if profil_pixmap.isNull():
                profil_pixmap = hologram_ikon_olustur(36, "#0078D4", "#FFFFFF", "U")
        else:
            profil_pixmap = QPixmap("src/model/yapay_zeka_ikon.png")
            if profil_pixmap.isNull():
                profil_pixmap = hologram_ikon_olustur(36, "#0078D4", "#FFFFFF", "AI")
        
        profil_pixmap = profil_pixmap.scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        profil_ikon.setPixmap(profil_pixmap)
        profil_duzen.addWidget(profil_ikon)
        
        baslik_widget = QWidget(self)
        baslik_duzen = QVBoxLayout(baslik_widget)
        baslik_duzen.setContentsMargins(0, 0, 0, 0)
        baslik_duzen.setSpacing(2)
        
        baslik = QLabel(self.gonderici.capitalize(), baslik_widget)
        baslik.setStyleSheet(f"color: {renkler['metin']}; font-weight: 600; font-size: 13px;")
        
        saat = QLabel(time.strftime("%H:%M"), baslik_widget)
        saat.setStyleSheet(f"color: {renkler['metin_ikincil']}; font-size: 11px;")
        
        baslik_duzen.addWidget(baslik)
        baslik_duzen.addWidget(saat)
        
        ust_duzen.addWidget(profil_widget)
        ust_duzen.addWidget(baslik_widget)
        ust_duzen.addStretch()
        
        duzen.addLayout(ust_duzen)
        
        self.metin = self.metin.replace('\n', '<br>')
        
        import re
        url_pattern = r'(https?://\S+)'
        self.metin = re.sub(url_pattern, 
                           lambda m: f'<a href="{m.group(1)}" style="color: {renkler["vurgu"]}; text-decoration: none;">{m.group(1)}</a>', 
                           self.metin)
        
        mesaj_cerceve = QFrame(self)
        mesaj_cerceve.setObjectName("mesajCerceve")
        
        mesaj_duzen = QVBoxLayout(mesaj_cerceve)
        mesaj_duzen.setContentsMargins(16, 12, 16, 12)
        
        mesaj_etiket = QLabel(self.metin, mesaj_cerceve)
        mesaj_etiket.setTextFormat(Qt.TextFormat.RichText)
        mesaj_etiket.setOpenExternalLinks(True)
        mesaj_etiket.setWordWrap(True)
        mesaj_etiket.setStyleSheet(f"color: {renkler['metin']}; font-size: 14px; line-height: 145%;")
        mesaj_duzen.addWidget(mesaj_etiket)
        
        duzen.addWidget(mesaj_cerceve)
        
        arkaplan_renk = renkler['kullanici_mesaj'] if self.gonderici == "kullanici" else renkler['yapay_zeka_mesaj']
        kenar_renk = renkler['kenar']
        
        mesaj_cerceve.setStyleSheet(f"""
            QFrame#mesajCerceve {{
                background-color: {arkaplan_renk};
                border-radius: 10px;
                border: 1px solid {kenar_renk};
            }}
        """)
        
        profil_widget.setStyleSheet(f"""
            QFrame#profilWidget {{
                background-color: {renkler['vurgu']};
                border-radius: 18px;
            }}
        """)
        
        if self.gonderici == "kullanici":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            mesaj_etiket.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            mesaj_etiket.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

class DusunmeAnimasyon(QFrame):
    def __init__(self, parent=None, tema_yonetici=None):
        super().__init__(parent)
        self.tema_yonetici = tema_yonetici
        self.setMinimumHeight(80)
        self.setMaximumHeight(120)
        self.setMaximumWidth(600)
        
        self.nokta_animasyonlar = []
        self.nokta_timer = None
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        
        self.kurulum()
        self.animasyonBaslat()
    
    def animasyonBaslat(self):
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        self.anim.setDuration(200)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()
        
        self.noktaAnimasyonlariniBaslat()
    
    def kurulum(self):
        renkler = self.tema_yonetici.renkleri_al() if self.tema_yonetici else {
            "panel": "#FFFFFF",
            "panel_sekonder": "#F5F5F9",
            "vurgu": "#0078D4",
            "metin": "#202020",
            "metin_ikincil": "#5D5D5D",
            "kenar": "#E6E6E6",
            "golge": "rgba(0, 0, 0, 0.08)"
        }
        
        self.setObjectName("dusunmeAnimasyon")
        self.setStyleSheet(f"""
            QFrame#dusunmeAnimasyon {{
                background-color: {renkler['panel_sekonder']};
                border-radius: 12px;
                border: 1px solid {renkler['kenar']};
            }}
            QLabel {{
                color: {renkler['metin']};
                background: transparent;
            }}
        """)
        
        duzen = QVBoxLayout(self)
        duzen.setContentsMargins(20, 16, 20, 16)
        duzen.setSpacing(12)
        
        ust_duzen = QHBoxLayout()
        ust_duzen.setContentsMargins(0, 0, 0, 0)
        ust_duzen.setSpacing(12)
        
        dusunme_ikon = QLabel(self)
        dusunme_ikon.setFixedSize(24, 24)
        
        try:
            ikon = QPixmap("src/model/dusunme_ikonu.png")
            if not ikon.isNull():
                ikon = ikon.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                dusunme_ikon.setPixmap(ikon)
            else:
                dusunme_ikon_pixmap = hologram_ikon_olustur(24, renkler['vurgu'], "#FFFFFF", "🔄")
                dusunme_ikon.setPixmap(dusunme_ikon_pixmap)
        except:
            dusunme_ikon_pixmap = hologram_ikon_olustur(24, renkler['vurgu'], "#FFFFFF", "🔄")
            dusunme_ikon.setPixmap(dusunme_ikon_pixmap)
        
        self.metinSahasi = QLabel("Düşünüyor...", self)
        self.metinSahasi.setStyleSheet(f"font-weight: 600; font-size: 15px; color: {renkler['metin']};")
        self.metinSahasi.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        ust_duzen.addWidget(dusunme_ikon)
        ust_duzen.addWidget(self.metinSahasi)
        ust_duzen.addStretch()
        
        duzen.addLayout(ust_duzen)
        
        nokta_container = QFrame(self)
        nokta_container.setObjectName("noktaContainer")
        nokta_container.setStyleSheet(f"""
            QFrame#noktaContainer {{
                background-color: {renkler['panel']};
                border-radius: 10px;
                border: 1px solid {renkler['kenar']};
                padding: 4px;
            }}
        """)
        
        nokta_duzen = QHBoxLayout(nokta_container)
        nokta_duzen.setSpacing(12)
        nokta_duzen.setContentsMargins(16, 8, 16, 8)
        nokta_duzen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        for i in range(3):
            nokta = QLabel("•", self)
            nokta.setFixedSize(24, 24)
            nokta.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nokta.setStyleSheet(f"""
                QLabel {{
                    color: {renkler['vurgu']};
                    font-size: 28px;
                    font-weight: bold;
                }}
            """)
            nokta_duzen.addWidget(nokta)
            self.nokta_animasyonlar.append(nokta)
        
        duzen.addWidget(nokta_container)
    
    def noktaAnimasyonlariniBaslat(self):
        if self.nokta_timer is None:
            self.nokta_timer = QTimer(self)
            self.nokta_timer.timeout.connect(self.zamanAsi)
            self.nokta_timer.start(300)
    
    def zamanAsi(self):
        for i, nokta in enumerate(self.nokta_animasyonlar):
            QTimer.singleShot(i*100, lambda n=nokta: self.noktaAnimasyonu(n))
    
    def noktaAnimasyonu(self, nokta):
        anim = QPropertyAnimation(nokta, b"geometry", self)
        anim.setDuration(300)
        baslangic_geo = nokta.geometry()
        
        yukarı_geo = QRect(
            int(baslangic_geo.x()),
            int(baslangic_geo.y() - 12),
            int(baslangic_geo.width()),
            int(baslangic_geo.height())
        )
        
        anim.setStartValue(baslangic_geo)
        anim.setEndValue(yukarı_geo)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        geri_anim = QPropertyAnimation(nokta, b"geometry", self)
        geri_anim.setDuration(300)
        geri_anim.setStartValue(yukarı_geo)
        geri_anim.setEndValue(baslangic_geo)
        geri_anim.setEasingCurve(QEasingCurve.Type.InQuad)
        
        seq = QSequentialAnimationGroup(self)
        seq.addAnimation(anim)
        seq.addAnimation(geri_anim)
        seq.start()
    
    def closeEvent(self, event):
        if self.nokta_timer:
            self.nokta_timer.stop()
            self.nokta_timer = None
        super().closeEvent(event)

class ModelGorunumBasic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 480)
        self.hata_mesaji = None
        self.kurulum()
    
    def kurulum(self):
        self.duzen = QVBoxLayout(self)
        self.duzen.setContentsMargins(0, 0, 0, 0)
        
        try:
            self.hata_mesaji = QLabel("Model görünümü yüklenemedi.\nLütfen bağlantınızı kontrol edin.")
            self.hata_mesaji.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hata_mesaji.setStyleSheet("""
                background-color: #3B4252;
                color: #ECEFF4;
                border-radius: 15px;
                padding: 20px;
                font-size: 14px;
            """)
            self.duzen.addWidget(self.hata_mesaji)
        except Exception as e:
            print(f"Model görünümü yüklenirken hata: {str(e)}")

    def konusmaBaslat(self):
        pass

    def konusmaBitir(self):
        pass

class CanliKonusmaWidget(QFrame):
    def __init__(self, parent=None, tema_yonetici=None):
        super().__init__(parent)
        self.tema_yonetici = tema_yonetici
        self.setMaximumHeight(100)
        self.kurulum()
        
    def kurulum(self):
        renkler = self.tema_yonetici.renkleri_al() if self.tema_yonetici else {
            "panel": "#FFFFFF", 
            "panel_sekonder": "#F5F5F9",
            "vurgu": "#0078D4",
            "metin": "#202020", 
            "metin_ikincil": "#5D5D5D",
            "kenar": "#E6E6E6"
        }
        
        self.setObjectName("canliKonusmaWidget")
        self.setStyleSheet(f"""
            QFrame#canliKonusmaWidget {{
                background-color: {renkler['panel_sekonder']};
                border-radius: 12px;
                border: 1px solid {renkler['kenar']};
            }}
        """)
        
        self.duzen = QHBoxLayout(self)
        self.duzen.setContentsMargins(16, 10, 16, 10)
        self.duzen.setSpacing(12)

        dalga_konteyner = QFrame(self)
        dalga_konteyner.setObjectName("dalgaKonteyner")
        dalga_konteyner.setFixedSize(40, 40)
        dalga_konteyner.setStyleSheet(f"""
            QFrame#dalgaKonteyner {{
                background-color: {renkler['vurgu']};
                border-radius: 20px;
            }}
        """)
        
        dalga_duzen = QVBoxLayout(dalga_konteyner)
        dalga_duzen.setContentsMargins(0, 0, 0, 0)
        
        mikrofon_ikon = QLabel(dalga_konteyner)
        mikrofon_ikon.setFixedSize(24, 24)
        mikrofon_ikon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        try:
            ikon = QPixmap("src/model/mikrofon_ikonu.png")
            if not ikon.isNull():
                ikon = ikon.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                mikrofon_ikon.setPixmap(ikon)
            else:
                mikrofon_pixmap = hologram_ikon_olustur(20, "#FFFFFF", renkler['vurgu'], "🎤")
                mikrofon_ikon.setPixmap(mikrofon_pixmap)
        except:
            mikrofon_pixmap = hologram_ikon_olustur(20, "#FFFFFF", renkler['vurgu'], "🎤")
            mikrofon_ikon.setPixmap(mikrofon_pixmap)
        
        dalga_duzen.addWidget(mikrofon_ikon)
        
        bilgi_container = QFrame(self)
        bilgi_duzen = QVBoxLayout(bilgi_container)
        bilgi_duzen.setContentsMargins(0, 0, 0, 0)
        bilgi_duzen.setSpacing(4)
        
        self.metin_etiketi = QLabel("Dinleniyor...", bilgi_container)
        self.metin_etiketi.setStyleSheet(f"""
            color: {renkler['metin']};
            font-size: 15px;
            font-weight: 600;
        """)
        
        aciklama_etiketi = QLabel("Konuşmayı algılamak için mikrofona konuşun", bilgi_container)
        aciklama_etiketi.setStyleSheet(f"""
            color: {renkler['metin_ikincil']};
            font-size: 12px;
        """)
        
        bilgi_duzen.addWidget(self.metin_etiketi)
        bilgi_duzen.addWidget(aciklama_etiketi)
        
        self.duzen.addWidget(dalga_konteyner)
        self.duzen.addWidget(bilgi_container)
        self.duzen.addStretch()
        
        iptal_buton = QPushButton("İptal", self)
        iptal_buton.setFixedSize(80, 36)
        iptal_buton.setCursor(Qt.CursorShape.PointingHandCursor)
        iptal_buton.setStyleSheet(f"""
            QPushButton {{
                background-color: {renkler['buton']};
                color: {renkler['metin']};
                border: 1px solid {renkler['kenar']};
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {renkler['buton_hover']};
            }}
            QPushButton:pressed {{
                background-color: {renkler['vurgu']};
                color: white;
            }}
        """)
        iptal_buton.clicked.connect(self.gizle)
        
        self.duzen.addWidget(iptal_buton)

        self.dalga_anim_grup = QParallelAnimationGroup(self)

        self.dalga_anim = QPropertyAnimation(dalga_konteyner, b"styleSheet", self)
        self.dalga_anim.setDuration(1000)
        self.dalga_anim.setStartValue(f"""
            QFrame#dalgaKonteyner {{
                background-color: {renkler['vurgu']};
                border-radius: 20px;
            }}
        """)
        self.dalga_anim.setEndValue(f"""
            QFrame#dalgaKonteyner {{
                background-color: {renkler['metin_ikincil']};
                border-radius: 20px;
            }}
        """)
        self.dalga_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.dalga_anim_grup.addAnimation(self.dalga_anim)
        self.dalga_anim_grup.setLoopCount(-1)
    
    def metniGuncelle(self, metin):
        self.metin_etiketi.setText(metin)
    
    def gizle(self):
        self.dalga_anim_grup.stop()
        self.hide()
    
    def goster(self):
        self.show()
        self.dalga_anim_grup.start()

class AnaForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GPT Sohbet Asistanı")
        self.gpt = GPTBaglanti()
        
        self.tema_yonetici = TemaYoneticisi()
        self.renkler = self.tema_yonetici.renkleri_al()
        
        self.detayli_dusunme = False
        self.web_arama = False
        self.aktif_mod = "normal"
        self.mesajListesiDuzen = None
        self.aktif_sohbet_id = None
        self.dusunmeAnimasyonu = None
        self.mesajlasma_daraltildi = False
        self.model_acik = True
        
        try:
            self.dosyalari_kontrol_et()
            self.ikonlariOlustur()
            self.kurulum()
            self.tema_uygula()
            
            QTimer.singleShot(1000, self.ilk_sohbet_kontrolu)
        except Exception as e:
            import traceback
            print(f"Başlatma hatası: {str(e)}")
            print(traceback.format_exc())
            self.hataMesajiGoster(f"Uygulama başlatılamadı: {str(e)}")
    
    def tema_uygula(self):
        css = self.tema_yonetici.css_degiskenler()
        self.setStyleSheet(css)
        self.renkler = self.tema_yonetici.renkleri_al()
        
        for widget in self.findChildren(QFrame) + self.findChildren(QWidget):
            if hasattr(widget, "setProperty"):
                widget.setProperty("tema", self.tema_yonetici.aktif_tema)
                widget.style().unpolish(widget)
                widget.style().polish(widget)
                
        for widget in self.findChildren(QScrollArea):
            widget.setStyleSheet(f"""
                QScrollArea {{ 
                    background-color: {self.renkler['panel']}; 
                    border: none; 
                }}
                QScrollBar:vertical {{
                    background-color: {self.renkler['panel']};
                    width: 8px;
                    margin: 0px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: {self.renkler['kenar']};
                    border-radius: 4px;
                    min-height: 20px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                    height: 0px;
                }}
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                    background: none;
                }}
            """)
        
        if hasattr(self, 'ust_cubuk'):
            self.ust_cubuk.setStyleSheet(f"""
                QFrame#ust_cubuk {{
                    background-color: {self.renkler['panel']};
                    border-radius: 10px;
                    border: 1px solid {self.renkler['kenar']};
                }}
            """)
            
        if hasattr(self, 'mesajlasmaAlani'):
            self.mesajlasmaAlani.setStyleSheet(f"""
                QScrollArea {{
                    background-color: {self.renkler['arkaplan']};
                    border-radius: 10px;
                    border: 1px solid {self.renkler['kenar']};
                }}
                QWidget#mesajlasmaIcerik {{
                    background-color: {self.renkler['arkaplan']};
                }}
            """)
            
        if hasattr(self, 'yazismaAlani'):
            self.yazismaAlani.setStyleSheet(f"""
                QFrame#yazismaAlani {{
                    background-color: {self.renkler['panel']};
                    border-radius: 10px;
                    border: 1px solid {self.renkler['kenar']};
                }}
            """)
            
        if hasattr(self, 'mesajGiris'):
            self.mesajGiris.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {self.renkler['panel_sekonder']};
                    border-radius: 8px;
                    color: {self.renkler['metin']};
                    border: 1px solid {self.renkler['kenar']};
                    padding: 8px;
                }}
            """)
            
        if hasattr(self, 'sohbetYonetimiKonteyner'):
            self.sohbetYonetimiKonteyner.setStyleSheet(f"""
                QFrame#sohbetYonetimiKonteyner {{
                    background-color: {self.renkler['panel']};
                    border-radius: 10px;
                    border: 1px solid {self.renkler['kenar']};
                }}
            """)
        
        if hasattr(self, 'sohbetYonetici'):
            self.sohbetYonetici.tema_degistir(self.tema_yonetici.aktif_tema, self.renkler)
    
    def tema_degistir(self):
        try:
            yeni_tema = "koyu" if self.tema_yonetici.aktif_tema == "acik" else "acik"
            self.tema_yonetici.tema_degistir(yeni_tema)
            
            tema_ikonu = self.gunesIkon if yeni_tema == "koyu" else self.ayIkon
            if hasattr(self, 'tema_buton'):
                self.tema_buton.setIcon(tema_ikonu)
                
            QTimer.singleShot(100, self.tema_uygula)
        except Exception as e:
            print(f"Tema değiştirme hatası: {str(e)}")
    
    def dosyalari_kontrol_et(self):
        model_klasoru = os.path.join(os.getcwd(), "model")
        if not os.path.exists(model_klasoru):
            os.makedirs(model_klasoru)
            
        gerekli_dosya_listesi = [
            "uygulama_ikonu.png",
            "yapay_zeka_ikon.png",
            "kullanici_ikon.png",
            "dusunme_ikonu.png",
            "gonder_ikonu.png",
            "mikrofon_ikonu.png",
            "sil_ikonu.png",
            "duzenle_ikonu.png",
            "daralt_ikonu.png",
            "genislet_ikonu.png"
        ]
        
        eksik_dosyalar = []
        for dosya in gerekli_dosya_listesi:
            if not os.path.exists(os.path.join(model_klasoru, dosya)):
                eksik_dosyalar.append(dosya)
        
        if eksik_dosyalar:
            dosyalari_olustur_ve_kaydet()
    
    def ilk_sohbet_kontrolu(self):
        try:
            if not hasattr(self, 'sohbetYonetici') or self.sohbetYonetici is None:
                return
                
            self.sohbetYonetici.sohbet_listesini_guncelle()
            
            if len(self.sohbetYonetici.sohbetler) == 0:
                self.yeniSohbetBaslat()
            elif not self.aktif_sohbet_id and len(self.sohbetYonetici.sohbetler) > 0:
                ilk_sohbet_id = list(self.sohbetYonetici.sohbetler.keys())[0]
                self.sohbetYonetici.sohbetSec(ilk_sohbet_id)
                self.aktif_sohbet_id = ilk_sohbet_id
                self.yazisma_alani_goster(True)
                
        except Exception as e:
            print(f"Sohbet başlatma hatası: {str(e)}")
            QTimer.singleShot(2000, self.ilk_sohbet_kontrolu)
    
    def sohbet_degisti(self, sohbet_id):
        try:
            self.aktif_sohbet_id = sohbet_id
            if self.mesajListesiDuzen is not None:
                for i in reversed(range(self.mesajListesiDuzen.count())):
                    widget = self.mesajListesiDuzen.itemAt(i).widget()
                    if widget is not None:
                        widget.setParent(None)
                
                for mesaj in self.sohbetYonetici.aktif_sohbet_mesajlari():
                    self.mesajEkle(mesaj["metin"], mesaj["gonderen"])
        except Exception as e:
            print(f"Sohbet değişim hatası: {str(e)}")
            
    def ikonlariOlustur(self):
        try:
            ikon_boyut = QSize(24, 24)
            ikon_yolu = "model/"
            
            ikon_dosyalari = {
                "gonder_ikonu.png": "➤",
                "mikrofon_ikonu.png": "🎤",
                "sil_ikonu.png": "🗑️",
                "duzenle_ikonu.png": "✏️",
                "daralt_ikonu.png": "◀",
                "genislet_ikonu.png": "▶",
                "uygulama_ikonu.png": "AI",
                "yapay_zeka_ikon.png": "🤖",
                "kullanici_ikon.png": "👤",
                "dusunme_ikonu.png": "⟳"
            }
            
            for dosya, karakter in ikon_dosyalari.items():
                dosya_yolu = os.path.join(ikon_yolu, dosya)
                if not os.path.exists(dosya_yolu) or os.path.getsize(dosya_yolu) < 100:
                    self._create_icon_file(dosya_yolu, karakter)
            
            self.gonderIkon = QIcon(os.path.join(ikon_yolu, "gonder_ikonu.png"))
            self.mikrofonIkon = QIcon(os.path.join(ikon_yolu, "mikrofon_ikonu.png"))
            self.silIkon = QIcon(os.path.join(ikon_yolu, "sil_ikonu.png"))
            self.duzenleIkon = QIcon(os.path.join(ikon_yolu, "duzenle_ikonu.png"))
            self.daraltIkon = QIcon(os.path.join(ikon_yolu, "daralt_ikonu.png"))
            self.genisletIkon = QIcon(os.path.join(ikon_yolu, "genislet_ikonu.png"))
            self.uygulamaIkon = QIcon(os.path.join(ikon_yolu, "uygulama_ikonu.png"))
            self.yapayZekaIkon = QIcon(os.path.join(ikon_yolu, "yapay_zeka_ikon.png"))
            self.kullaniciIkon = QIcon(os.path.join(ikon_yolu, "kullanici_ikon.png"))
            self.dusunmeIkon = QIcon(os.path.join(ikon_yolu, "dusunme_ikonu.png"))
            
            ikon_renk = "#ECEFF4"
            self.yeniIkon = self._createIcon("✚", ikon_renk, ikon_boyut)
            self.webIkon = self._createIcon("🔍", ikon_renk, ikon_boyut)
            self.normalIkon = self._createIcon("💬", ikon_renk, ikon_boyut)
            self.edebiIkon = self._createIcon("📝", ikon_renk, ikon_boyut)
            self.ogreticiIkon = self._createIcon("🎓", ikon_renk, ikon_boyut)
            self.detayliIkon = self._createIcon("🧠", ikon_renk, ikon_boyut)
            self.ayIkon = self._createIcon("🌙", ikon_renk, ikon_boyut)
            self.gunesIkon = self._createIcon("☀️", ikon_renk, ikon_boyut)
            
        except Exception as e:
            print(f"İkonlar yüklenirken hata: {str(e)}")
    
    def _create_icon_file(self, dosya_yolu, karakter):
        try:
            os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
            
            boyut = QSize(64, 64)
            renkler = self.tema_yonetici.renkleri_al()
            
            pixmap = QPixmap(boyut)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

            if dosya_yolu.endswith("duzenle_ikonu.png"):
                painter.setPen(QPen(QColor(renkler["vurgu"]), 3))
                painter.drawLine(16, 48, 48, 16)
                painter.drawLine(16, 48, 24, 48)
                painter.drawLine(16, 48, 16, 40)
                painter.drawLine(44, 20, 48, 16)
            elif dosya_yolu.endswith("sil_ikonu.png"):
                painter.setPen(QPen(QColor(renkler["hata"]), 3))
                painter.drawRect(16, 16, 32, 36)
                painter.drawLine(16, 16, 32, 10)
                painter.drawLine(48, 16, 32, 10)
                painter.drawLine(24, 26, 24, 42)
                painter.drawLine(32, 26, 32, 42)
                painter.drawLine(40, 26, 40, 42)
            elif dosya_yolu.endswith("daralt_ikonu.png"):
                painter.setBrush(QColor(renkler["vurgu"]))
                painter.setPen(Qt.PenStyle.NoPen)
                
                yol = QPainterPath()
                yol.moveTo(40, 16)
                yol.lineTo(24, 32)
                yol.lineTo(40, 48)
                yol.closeSubpath()
                
                painter.drawPath(yol)
            elif dosya_yolu.endswith("genislet_ikonu.png"):
                painter.setBrush(QColor(renkler["vurgu"]))
                painter.setPen(Qt.PenStyle.NoPen)
                
                yol = QPainterPath()
                yol.moveTo(24, 16)
                yol.lineTo(40, 32)
                yol.lineTo(24, 48)
                yol.closeSubpath()
                
                painter.drawPath(yol)
            else:
                font = QFont("Segoe UI", 32, QFont.Weight.Bold)
                painter.setFont(font)
                painter.setPen(QColor(renkler["vurgu"]))
                painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, karakter)
            
            painter.end()
            pixmap.save(dosya_yolu, "PNG")
            print(f"İkon oluşturuldu: {dosya_yolu}")
            return True
        except Exception as e:
            print(f"İkon oluşturma hatası: {str(e)}")
            return False
    
    def kurulum(self):
        merkez_widget = QWidget(self)
        merkez_widget.setObjectName("merkez_widget")
        ana_duzen = QVBoxLayout(merkez_widget)
        ana_duzen.setContentsMargins(16, 16, 16, 16)
        ana_duzen.setSpacing(16)
        
        ust_cubuk = QFrame(merkez_widget)
        ust_cubuk.setObjectName("ust_cubuk")
        ust_cubuk.setFixedHeight(50)
        ust_cubuk.setStyleSheet(f"""
            QFrame#ust_cubuk {{
                background-color: {self.renkler['panel']};
                border-radius: 10px;
                border: 1px solid {self.renkler['kenar']};
            }}
        """)
        
        ust_duzen = QHBoxLayout(ust_cubuk)
        ust_duzen.setContentsMargins(16, 8, 16, 8)
        
        logo_etiket = QLabel(ust_cubuk)
        logo_pixmap = QPixmap("src/model/uygulama_ikonu.png")
        if logo_pixmap.isNull():
            logo_pixmap = hologram_ikon_olustur(32, "#0078D4", "#FFFFFF", "AI")
        logo_pixmap = logo_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_etiket.setPixmap(logo_pixmap)
        logo_etiket.setFixedSize(32, 32)
        
        baslik_etiket = QLabel("GPT Karşılıklı Sohbet", ust_cubuk)
        baslik_etiket.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {self.renkler['metin']};")
        
        ust_duzen.addWidget(logo_etiket)
        ust_duzen.addSpacing(10)
        ust_duzen.addWidget(baslik_etiket)
        ust_duzen.addStretch()
        
        mod_grup = QButtonGroup(self)
        
        self.normal_mod_buton = QPushButton("Normal", ust_cubuk)
        self.normal_mod_buton.setCheckable(True)
        self.normal_mod_buton.setChecked(True)
        self.normal_mod_buton.clicked.connect(lambda: self.modDegistir("normal"))
        
        self.edebi_mod_buton = QPushButton("Edebi", ust_cubuk)
        self.edebi_mod_buton.setCheckable(True)
        self.edebi_mod_buton.clicked.connect(lambda: self.modDegistir("edebi"))
        
        self.ogretici_mod_buton = QPushButton("Öğretici", ust_cubuk)
        self.ogretici_mod_buton.setCheckable(True)
        self.ogretici_mod_buton.clicked.connect(lambda: self.modDegistir("ogretici"))
        
        mod_grup.addButton(self.normal_mod_buton)
        mod_grup.addButton(self.edebi_mod_buton)
        mod_grup.addButton(self.ogretici_mod_buton)
        
        for buton in [self.normal_mod_buton, self.edebi_mod_buton, self.ogretici_mod_buton]:
            buton.setFixedHeight(36)
            buton.setCursor(Qt.CursorShape.PointingHandCursor)
            ust_duzen.addWidget(buton)
        
        ust_duzen.addSpacing(20)
        
        self.detayli_dusunme_buton = QPushButton("🧠 Detaylı Düşünme", ust_cubuk)
        self.detayli_dusunme_buton.setCheckable(True)
        self.detayli_dusunme_buton.clicked.connect(self.detayliDusunmeDegistir)
        
        self.web_arama_buton = QPushButton("🔍 Web Arama", ust_cubuk)
        self.web_arama_buton.setCheckable(True)
        self.web_arama_buton.clicked.connect(self.webAramaDegistir)
        
        for buton in [self.detayli_dusunme_buton, self.web_arama_buton]:
            buton.setFixedHeight(36)
            buton.setCursor(Qt.CursorShape.PointingHandCursor)
            ust_duzen.addWidget(buton)
        
        self.tema_buton = QPushButton(ust_cubuk)
        self.tema_buton.setIcon(self.gunesIkon if self.tema_yonetici.aktif_tema == "koyu" else self.ayIkon)
        self.tema_buton.setIconSize(QSize(20, 20))
        self.tema_buton.setFixedSize(36, 36)
        self.tema_buton.setToolTip("Tema Değiştir")
        self.tema_buton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tema_buton.clicked.connect(self.tema_degistir)
        ust_duzen.addWidget(self.tema_buton)
        
        ana_duzen.addWidget(ust_cubuk)
        
        icerik_alani = QFrame(merkez_widget)
        icerik_alani.setObjectName("icerikAlani")
        icerik_duzen = QHBoxLayout(icerik_alani)
        icerik_duzen.setContentsMargins(0, 0, 0, 0)
        icerik_duzen.setSpacing(16)
        
        self.sohbetYonetimiKonteyner = QFrame(icerik_alani)
        self.sohbetYonetimiKonteyner.setObjectName("sohbetYonetimiKonteyner")
        self.sohbetYonetimiKonteyner.setMinimumWidth(250)
        self.sohbetYonetimiKonteyner.setMaximumWidth(350)
        
        sohbetKonteynerDuzen = QHBoxLayout(self.sohbetYonetimiKonteyner)
        sohbetKonteynerDuzen.setContentsMargins(0, 0, 0, 0)
        sohbetKonteynerDuzen.setSpacing(0)
        
        self.sohbetYonetici = SohbetYonetici(self.sohbetYonetimiKonteyner)
        self.sohbetYonetici.sohbetDegisti.connect(self.sohbet_degisti)
        self.sohbetYonetici.set_gpt_baglanti(self.gpt)
        sohbetKonteynerDuzen.addWidget(self.sohbetYonetici)
        
        self.sohbetDaraltButon = QPushButton(self.sohbetYonetimiKonteyner)
        self.sohbetDaraltButon.setObjectName("sohbetDaraltButon")
        self.sohbetDaraltButon.setIcon(self.daraltIkon)
        self.sohbetDaraltButon.setFixedSize(24, 80)
        self.sohbetDaraltButon.setIconSize(QSize(12, 12))
        self.sohbetDaraltButon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sohbetDaraltButon.clicked.connect(self.sohbetPaneliDaraltGenislet)
        self.sohbetDaraltButon.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.1);
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        self.sohbetDaraltButon.hide()
        sohbetKonteynerDuzen.addWidget(self.sohbetDaraltButon)
        
        icerik_duzen.addWidget(self.sohbetYonetimiKonteyner)
        
        icerik_splitter = QSplitter(Qt.Orientation.Horizontal, icerik_alani)
        icerik_splitter.setChildrenCollapsible(False)
        
        self.modelPanel = QFrame(icerik_splitter)
        self.modelPanel.setObjectName("modelPanel")
        self.modelPanel.setMinimumWidth(360)
        
        self.modelPanel.setStyleSheet(f"""
            QFrame#modelPanel {{
                background-color: {self.renkler['panel_sekonder']};
                border-radius: 10px;
                border: 1px solid {self.renkler['kenar']};
            }}
        """)
        
        modelDuzen = QVBoxLayout(self.modelPanel)
        modelDuzen.setContentsMargins(0, 0, 0, 0)
        
        self.modelGorunum = ModelGorunum3D(self.modelPanel)
        modelDuzen.addWidget(self.modelGorunum)
        
        self.mesajlasmaPanel = QFrame(icerik_splitter)
        self.mesajlasmaPanel.setObjectName("mesajlasmaPanel")
        self.mesajlasmaPanel.setMinimumWidth(480)
        
        self.mesajlasmaPanel.setStyleSheet(f"""
            QFrame#mesajlasmaPanel {{
                background-color: {self.renkler['panel']};
                border-radius: 10px;
                border: 1px solid {self.renkler['kenar']};
            }}
        """)
        
        mesajlasmaLayout = QVBoxLayout(self.mesajlasmaPanel)
        mesajlasmaLayout.setContentsMargins(0, 0, 0, 0)
        mesajlasmaLayout.setSpacing(0)
        
        mesajlasmaUstDuzen = QHBoxLayout()
        mesajlasmaUstDuzen.setContentsMargins(16, 12, 16, 12)
        
        mesajlasmaBaslik = QLabel("Sohbet", self.mesajlasmaPanel)
        mesajlasmaBaslik.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        mesajlasmaBaslik.setStyleSheet(f"color: {self.renkler['metin']};")
        
        self.mesajlasmaDaraltButon = QPushButton(self.mesajlasmaPanel)
        self.mesajlasmaDaraltButon.setIcon(self.daraltIkon)
        self.mesajlasmaDaraltButon.setFixedSize(32, 32)
        self.mesajlasmaDaraltButon.setIconSize(QSize(16, 16))
        self.mesajlasmaDaraltButon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mesajlasmaDaraltButon.setToolTip("Panel Daralt")
        self.mesajlasmaDaraltButon.clicked.connect(self.mesajlasma_daralt_genislet)
        self.mesajlasmaDaraltButon.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.renkler['buton_hover']};
            }}
        """)
        
        mesajlasmaUstDuzen.addWidget(mesajlasmaBaslik)
        mesajlasmaUstDuzen.addStretch()
        mesajlasmaUstDuzen.addWidget(self.mesajlasmaDaraltButon)
        
        mesajlasmaLayout.addLayout(mesajlasmaUstDuzen)
        
        self.mesajListesiScroll = QScrollArea(self.mesajlasmaPanel)
        self.mesajListesiScroll.setWidgetResizable(True)
        self.mesajListesiScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.mesajListesiScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mesajListesiScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        mesajListesiContainer = QWidget(self.mesajListesiScroll)
        self.mesajListesiDuzen = QVBoxLayout(mesajListesiContainer)
        self.mesajListesiDuzen.setContentsMargins(16, 16, 16, 16)
        self.mesajListesiDuzen.setSpacing(16)
        self.mesajListesiDuzen.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.mesajListesiScroll.setWidget(mesajListesiContainer)
        mesajlasmaLayout.addWidget(self.mesajListesiScroll, 1)
        
        self.yazismaAlani = QFrame(self.mesajlasmaPanel)
        self.yazismaAlani.setFixedHeight(120)
        self.yazismaAlani.setContentsMargins(16, 8, 16, 8)
        yazismaDuzen = QVBoxLayout(self.yazismaAlani)
        yazismaDuzen.setContentsMargins(0, 0, 0, 0)
        
        self.mesajGiris = QTextEdit(self.yazismaAlani)
        self.mesajGiris.setPlaceholderText("Bir mesaj yazın...")
        self.mesajGiris.setFixedHeight(80)
        self.mesajGiris.setStyleSheet(f"""
            border: 1px solid {self.renkler['kenar']};
            border-radius: 8px;
            padding: 8px;
            background-color: {self.renkler['panel_sekonder']};
            color: {self.renkler['metin']};
        """)
        
        butonDuzen = QHBoxLayout()
        butonDuzen.setContentsMargins(0, 8, 0, 0)
        
        self.mesajGonderButon = QPushButton("", self.yazismaAlani)
        self.mesajGonderButon.setObjectName("mesajGonderButon")
        self.mesajGonderButon.setIcon(QIcon("src/model/gonder_ikonu.png"))
        self.mesajGonderButon.setIconSize(QSize(20, 20))
        self.mesajGonderButon.setFixedSize(36, 36)
        self.mesajGonderButon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mesajGonderButon.clicked.connect(self.mesajGonder)
        
        self.sesliMesajButon = QPushButton(self.yazismaAlani)
        self.sesliMesajButon.setIcon(self.mikrofonIkon)
        self.sesliMesajButon.setFixedSize(36, 36)
        self.sesliMesajButon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sesliMesajButon.clicked.connect(self.sesliMesaj)
        
        butonDuzen.addWidget(self.sesliMesajButon)
        butonDuzen.addStretch()
        butonDuzen.addWidget(self.mesajGonderButon)
        
        yazismaDuzen.addWidget(self.mesajGiris)
        yazismaDuzen.addLayout(butonDuzen)
        
        mesajlasmaLayout.addWidget(self.yazismaAlani)
        
        self.canliKonusma = CanliKonusmaWidget(self.mesajlasmaPanel, self.tema_yonetici)
        self.canliKonusma.setVisible(False)
        mesajlasmaLayout.addWidget(self.canliKonusma)
        
        icerik_splitter.addWidget(self.modelPanel)
        icerik_splitter.addWidget(self.mesajlasmaPanel)
        icerik_splitter.setSizes([int(self.width() * 0.35), int(self.width() * 0.65)])
        
        icerik_duzen.addWidget(icerik_splitter)
        ana_duzen.addWidget(icerik_alani, 1)
        
        self.setCentralWidget(merkez_widget)
        self.mesajGiris.installEventFilter(self)
        
        self.sohbetPaneliDaraltildi = False
        self.mesajlasma_daraltildi = False
    
    def eventFilter(self, obj, event):
        if obj == self.mesajGiris and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.mesajGonder()
                return True
        return super().eventFilter(obj, event)
        
    def modDegistir(self, mod):
        self.aktif_mod = mod

        self.normal_mod_buton.setChecked(mod == "normal")
        self.edebi_mod_buton.setChecked(mod == "edebi")
        self.ogretici_mod_buton.setChecked(mod == "ogretici")
    
    def detayliDusunmeDegistir(self):
        self.detayli_dusunme = self.detayli_dusunme_buton.isChecked()
    
    def webAramaDegistir(self):
        self.web_arama = self.web_arama_buton.isChecked()
    
    def yeniSohbetBaslat(self):
        try:
            yeni_sohbet_id = self.gpt.yeniSohbetBaslat()
            if yeni_sohbet_id:
                self.aktif_sohbet_id = yeni_sohbet_id
                self.sohbetYonetici.sohbet_listesini_guncelle()
                self.yazisma_alani_goster(True)
                self.karsilamaMesajiEkle()
                return True
            else:
                self.hataMesajiGoster("Yeni sohbet başlatılamadı")
                return False
        except Exception as e:
            self.hataMesajiGoster(f"Sohbet başlatma hatası: {str(e)}")
            return False
    
    def yazisma_alani_goster(self, goster):
        if self.yazismaAlani:
            self.yazismaAlani.setVisible(goster)
    
    def karsilamaMesajiEkle(self):
        self.mesajEkle("Merhaba! Size nasıl yardımcı olabilirim?", "yapay_zeka")
    
    def mesajGonder(self):
        metin = self.mesajGiris.toPlainText().strip()
        if not metin:
            return
            
        if not hasattr(self, 'sohbetYonetici') or not self.sohbetYonetici or not self.aktif_sohbet_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir sohbet seçin veya yeni bir sohbet başlatın.")
            return
            
        self.mesajGiris.clear()
        self.mesajGiris.setFocus()
        
        self.mesajEkle(metin, "kullanici")
        
        self.mesajGonderButon.setEnabled(False)
        self.sesliMesajButon.setEnabled(False)
        self.mesajGiris.setEnabled(False)
        
        if not hasattr(self, 'dusunmeAnimasyonu') or not self.dusunmeAnimasyonu:
            self.dusunmeAnimasyonu = DusunmeAnimasyon(self, self.tema_yonetici)
            self.mesajListesiDuzen.addWidget(self.dusunmeAnimasyonu)
            self.dusunmeAnimasyonu.animasyonBaslat()
        
        if hasattr(self, 'modelGorunum'):
            QTimer.singleShot(100, lambda: self.modelGorunum.konusmaBaslat())
            
        if hasattr(self, 'canliKonusma'):
            self.canliKonusma.goster()
            
        self.yapayzekaCevapAl(metin)
    
    def yapayzekaCevapAl(self, metin):
        thread = threading.Thread(target=self._yapayzekaCevapIslem, args=(metin,), daemon=True)
        thread.start()
        
    def _yapayzekaCevapIslem(self, metin):
        try:
            sohbet_id = self.aktif_sohbet_id
            yanit = self.sohbetYonetici.mesaj_gonder(metin)
            
            if sohbet_id != self.aktif_sohbet_id:
                return
                
            QTimer.singleShot(0, lambda: self.dusunmeAnimasyonuKaldir(yanit))
        except Exception as e:
            QTimer.singleShot(0, lambda: self.hataMesajiGoster(f"Yapay zeka yanıt hatası: {str(e)}"))
            QTimer.singleShot(0, lambda: self.dusunmeAnimasyonuKaldir(None))
    
    def dusunmeAnimasyonuKaldir(self, yanit):
        try:
            if hasattr(self, 'dusunmeAnimasyonu') and self.dusunmeAnimasyonu:
                self.mesajListesiDuzen.removeWidget(self.dusunmeAnimasyonu)
                self.dusunmeAnimasyonu.deleteLater()
                self.dusunmeAnimasyonu = None
            
            if yanit:
                self.mesajEkle(yanit, "yapay_zeka")
            if hasattr(self, 'modelGorunum'):
                QTimer.singleShot(100, lambda: self.modelGorunum.konusmaBaslat())
                QTimer.singleShot(len(yanit) * 50, lambda: self.modelGorunum.konusmaBitir())

            if hasattr(self, 'canliKonusma'):
                self.canliKonusma.metniGuncelle(yanit)
                QTimer.singleShot(len(yanit) * 50 + 500, lambda: self.canliKonusma.gizle())
        except Exception as e:
            print(f"Animasyon kaldırma hatası: {str(e)}")
        finally:
            self.mesajGonderButon.setEnabled(True)
            self.sesliMesajButon.setEnabled(True)
            self.mesajGiris.setEnabled(True)
            
            def silme_islemi():
                if hasattr(self, 'dusunmeAnimasyonu') and self.dusunmeAnimasyonu:
                    try:
                        self.mesajListesiDuzen.removeWidget(self.dusunmeAnimasyonu)
                        self.dusunmeAnimasyonu.deleteLater()
                        self.dusunmeAnimasyonu = None
                    except:
                        pass
                    
                self.mesajGiris.setFocus()
            
            QTimer.singleShot(0, silme_islemi)
    
    def sesliMesaj(self):
        if not hasattr(self, 'sohbetYonetici') or not self.sohbetYonetici or not self.aktif_sohbet_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir sohbet seçin veya yeni bir sohbet başlatın.")
            return
        
        try:
            self.sesliMesajButon.setEnabled(False)
            self.mesajGonderButon.setEnabled(False)
            
            self.dusunmeAnimasyonu = DusunmeAnimasyon(self)
            self.dusunmeAnimasyonu.metinSahasi.setText("Dinleniyor...")
            
            if self.mesajListesiDuzen is not None:
                self.mesajListesiDuzen.addWidget(self.dusunmeAnimasyonu)
            
            try:
                import speech_recognition
                import pyttsx3
            except ImportError as e:
                QMessageBox.warning(self, "Modül Eksik", 
                    f"Ses tanıma için gerekli modül yüklü değil: {str(e)}\n\n"
                    "pip install SpeechRecognition pyttsx3 pyaudio komutlarını kullanarak yükleyebilirsiniz.")
                self.dusunmeAnimasyonuKaldir(None)
                self.sesliMesajButon.setEnabled(True)
                self.mesajGonderButon.setEnabled(True)
                return
            
            try:
                sesTanima = SesKomutTanima()
            except Exception as e:
                QMessageBox.warning(self, "Ses Tanıma Hatası", 
                    f"Ses tanıma sistemi başlatılamadı: {str(e)}\n\n"
                    "Muhtemelen mikrofon erişimi yok veya mikrofon bağlı değil.")
                self.dusunmeAnimasyonuKaldir(None)
                self.sesliMesajButon.setEnabled(True)
                self.mesajGonderButon.setEnabled(True)
                return
            
            def ses_tanima_islemi():
                try:
                    metin = sesTanima.dinle()
                    if metin:
                        self.mesajGiris.setText(metin)
                        QTimer.singleShot(500, self.mesajGonder)
                    else:
                        self.dusunmeAnimasyonuKaldir(None)
                        QMessageBox.information(self, "Bilgi", "Ses alınamadı veya anlaşılamadı.")
                except Exception as e:
                    self.dusunmeAnimasyonuKaldir(None)
                    QMessageBox.warning(self, "Hata", f"Ses tanıma hatası: {str(e)}")
                finally:
                    self.sesliMesajButon.setEnabled(True)
                    self.mesajGonderButon.setEnabled(True)
            
            threading.Thread(target=ses_tanima_islemi, daemon=True).start()
        except Exception as e:
            self.sesliMesajButon.setEnabled(True)
            self.mesajGonderButon.setEnabled(True)
            QMessageBox.warning(self, "Hata", f"Ses tanıma başlatılamadı: {str(e)}")

    def sohbetPaneliDaraltGenislet(self):
        sohbet_konteyner_en = self.sohbetYonetimiKonteyner.width()
        daralt = sohbet_konteyner_en > 250
        
        if daralt:
            hedef_en = 60
            ikon = QIcon("src/model/genislet_ikonu.png")
            tanim = "Sohbet Panelini Genişlet"
        else:
            hedef_en = 300
            ikon = QIcon("src/model/daralt_ikonu.png")
            tanim = "Sohbet Panelini Daralt"
        
        self.sohbetDaraltButon.setIcon(ikon)
        self.sohbetDaraltButon.setToolTip(tanim)
        
        anim_grup = QParallelAnimationGroup()
        
        sohbet_anim = QPropertyAnimation(self.sohbetYonetimiKonteyner, b"maximumWidth")
        sohbet_anim.setDuration(300)
        sohbet_anim.setStartValue(sohbet_konteyner_en)
        sohbet_anim.setEndValue(hedef_en)
        sohbet_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_grup.addAnimation(sohbet_anim)
        
        genislik_anim = QPropertyAnimation(self.sohbetYonetimiKonteyner, b"minimumWidth")
        genislik_anim.setDuration(300)
        genislik_anim.setStartValue(self.sohbetYonetimiKonteyner.minimumWidth())
        genislik_anim.setEndValue(hedef_en)
        genislik_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_grup.addAnimation(genislik_anim)
        
        anim_grup.finished.connect(lambda: self.sohbetYonetici.setVisible(not daralt))
        
        if hasattr(self, 'sohbetYonetici'):
            self.sohbetYonetici.panel_daralt_genislet_durumu(daralt)
        
        anim_grup.start()
        self.sohbet_daraltildi = daralt
    
    def mesajlasma_daralt_genislet(self):
        mesajlasma_en = self.mesajlasmaPanel.width()
        daralt = not self.mesajlasma_daraltildi
        
        if daralt:
            hedef_en = 50
            ikon = QIcon("src/model/genislet_ikonu.png")
            tanim = "Paneli Genişlet"
            model_hedef_en = int(self.width() * 0.9)
        else:
            hedef_en = int(self.width() * 0.6)
            ikon = QIcon("src/model/daralt_ikonu.png")
            tanim = "Paneli Daralt"
            model_hedef_en = int(self.width() * 0.4)
        
        self.mesajlasmaDaraltButon.setIcon(ikon)
        self.mesajlasmaDaraltButon.setToolTip(tanim)
        
        anim_grup = QParallelAnimationGroup()
        
        mesajlasma_anim = QPropertyAnimation(self.mesajlasmaPanel, b"minimumWidth")
        mesajlasma_anim.setDuration(300)
        mesajlasma_anim.setStartValue(mesajlasma_en)
        mesajlasma_anim.setEndValue(hedef_en)
        mesajlasma_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_grup.addAnimation(mesajlasma_anim)
        
        mesajlasma_max_anim = QPropertyAnimation(self.mesajlasmaPanel, b"maximumWidth")
        mesajlasma_max_anim.setDuration(300)
        mesajlasma_max_anim.setStartValue(mesajlasma_en)
        mesajlasma_max_anim.setEndValue(hedef_en)
        mesajlasma_max_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_grup.addAnimation(mesajlasma_max_anim)
        
        if hasattr(self, 'modelPanel'):
            model_anim = QPropertyAnimation(self.modelPanel, b"maximumWidth")
            model_anim.setDuration(300)
            model_anim.setStartValue(self.modelPanel.width())
            model_anim.setEndValue(model_hedef_en)
            model_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim_grup.addAnimation(model_anim)
            
            model_min_anim = QPropertyAnimation(self.modelPanel, b"minimumWidth")
            model_min_anim.setDuration(300)
            model_min_anim.setStartValue(self.modelPanel.minimumWidth())
            model_min_anim.setEndValue(200)
            model_min_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim_grup.addAnimation(model_min_anim)

            if daralt and hasattr(self, 'modelGorunum'):
                QTimer.singleShot(100, lambda: self.modelGorunum.setMinimumSize(640, 480))
            else:
                QTimer.singleShot(100, lambda: self.modelGorunum.setMinimumSize(320, 480))
        
        anim_grup.start()
        
        if hasattr(self, 'icerik_splitter'):
            QTimer.singleShot(350, lambda: self.icerik_splitter.setSizes([model_hedef_en, hedef_en]))
        
        self.mesajlasma_icerik_goster(not daralt)
        self.mesajlasma_daraltildi = daralt

    def mesajlasma_icerik_goster(self, goster):
        if hasattr(self, 'mesajListesiScroll'):
            self.mesajListesiScroll.setVisible(goster)
        if hasattr(self, 'yazismaAlani'):
            self.yazismaAlani.setVisible(goster)

    def _createIcon(self, text, color, size=QSize(24, 24)):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(color))
        painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
        painter.end()
        return QIcon(pixmap)

    def hataMesajiGoster(self, hata):
        try:
            QMessageBox.critical(self, "Hata", hata)
        except:
            print(f"Kritik hata: {hata}")
    
    def mesajEkle(self, metin, gonderici):
        try:
            if self.mesajListesiDuzen is None:
                return
            mesajKarti = MesajKarti(metin, gonderici, self, self.tema_yonetici)
            self.mesajListesiDuzen.addWidget(mesajKarti)
            if hasattr(self, 'sohbetYonetici') and self.sohbetYonetici is not None:
                self.sohbetYonetici.mesaj_ekle(metin, gonderici)

            QApplication.processEvents()
            scrollBar = self.mesajListesiScroll.verticalScrollBar()
            kart_anim = QPropertyAnimation(scrollBar, b"value", self)
            kart_anim.setDuration(300)
            kart_anim.setStartValue(scrollBar.value())
            kart_anim.setEndValue(scrollBar.maximum())
            kart_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            kart_anim.start()

            QTimer.singleShot(350, lambda: QApplication.processEvents())
        except Exception as e:
            print(f"Mesaj eklenirken hata: {str(e)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        pencere_genislik = self.width()
        pencere_yukseklik = self.height()
        
        if hasattr(self, 'icerik_splitter') and pencere_genislik > 0:
            aktif_boyutlar = self.icerik_splitter.sizes()
            if len(aktif_boyutlar) == 2:
                sol_panel = aktif_boyutlar[0]
                sag_panel = aktif_boyutlar[1]
                toplam = sol_panel + sag_panel
                
                if toplam > 0:
                    sol_oran = sol_panel / toplam
                    if sol_oran > 0.8:
                        yeni_sol = int(pencere_genislik * 0.75)
                        yeni_sag = pencere_genislik - yeni_sol
                        self.icerik_splitter.setSizes([yeni_sol, yeni_sag])
                    elif sol_oran < 0.2:
                        yeni_sol = int(pencere_genislik * 0.25)
                        yeni_sag = pencere_genislik - yeni_sol
                        self.icerik_splitter.setSizes([yeni_sol, yeni_sag])
        
        if hasattr(self, 'sohbetYonetimiKonteyner') and not getattr(self, 'sohbet_daraltildi', False):
            ideal_genislik = min(300, int(pencere_genislik * 0.2))
            self.sohbetYonetimiKonteyner.setFixedWidth(ideal_genislik)
        
        if hasattr(self, 'mesajlasmaPanel') and hasattr(self, 'modelGorunum'):
            sol_genislik = self.mesajlasmaPanel.width()
            sag_genislik = self.modelGorunum.width()
            
            if sol_genislik < 400 and sag_genislik > 200:
                self.modelGorunum.setMaximumWidth(200)
            elif sol_genislik > 800 and sag_genislik < 300:
                self.modelGorunum.setMaximumWidth(int(pencere_genislik * 0.3))

def hologram_ikon_olustur(boyut, renk, arka_plan_renk, metin):
    pixmap = QPixmap(boyut, boyut)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(arka_plan_renk))
    painter.drawEllipse(0, 0, boyut, boyut)
    painter.setPen(QColor(renk))
    font = QFont("Segoe UI", int(boyut/2), QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, metin)
    painter.end()
    return pixmap

def dosyalari_olustur_ve_kaydet():
    model_klasoru = os.path.join(os.getcwd(), "model")
    if not os.path.exists(model_klasoru):
        os.makedirs(model_klasoru)

    uygulama_ikon = hologram_ikon_olustur(64, "#FFFFFF", "#0078D4", "AI")
    uygulama_ikon.save(os.path.join(model_klasoru, "uygulama_ikonu.png"))
    yapay_zeka_ikon = hologram_ikon_olustur(36, "#FFFFFF", "#0078D4", "AI")
    yapay_zeka_ikon.save(os.path.join(model_klasoru, "yapay_zeka_ikon.png"))
    kullanici_ikon = hologram_ikon_olustur(36, "#FFFFFF", "#0078D4", "U")
    kullanici_ikon.save(os.path.join(model_klasoru, "kullanici_ikon.png"))
    dusunme_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#0078D4", "🔄")
    dusunme_ikon.save(os.path.join(model_klasoru, "dusunme_ikonu.png"))
    gonder_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#0078D4", "➤")
    gonder_ikon.save(os.path.join(model_klasoru, "gonder_ikonu.png"))
    mikrofon_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#0078D4", "🎤")
    mikrofon_ikon.save(os.path.join(model_klasoru, "mikrofon_ikonu.png"))
    sil_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#FF0000", "✖")
    sil_ikon.save(os.path.join(model_klasoru, "sil_ikonu.png"))
    duzenle_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#0078D4", "✎")
    duzenle_ikon.save(os.path.join(model_klasoru, "duzenle_ikonu.png"))
    daralt_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#0078D4", "◀")
    daralt_ikon.save(os.path.join(model_klasoru, "daralt_ikonu.png"))
    genislet_ikon = hologram_ikon_olustur(24, "#FFFFFF", "#0078D4", "▶")
    genislet_ikon.save(os.path.join(model_klasoru, "genislet_ikonu.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dosyalari_olustur_ve_kaydet()
    ana_form = AnaForm()
    ana_form.show()
    sys.exit(app.exec())