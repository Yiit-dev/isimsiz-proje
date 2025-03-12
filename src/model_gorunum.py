import sys
import numpy as np
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGraphicsOpacityEffect, QSizePolicy
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QFont, QPainter, QColor, QLinearGradient, QPen, QPainterPath
import math
import os

class ModelGorunum(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 480)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.hata_mesaji = None
        self.konusma_aktif = False
        self.animasyon_zamanlayici = None
        self.dalga_offset = 0
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        
        self.kurulum()
        self.giris_animasyonu_baslat()
        
    def kurulum(self):
        self.duzen = QVBoxLayout(self)
        self.duzen.setContentsMargins(0, 0, 0, 0)
        self.duzen.setSpacing(0)
        
        self.cerceve = QFrame()
        self.cerceve.setObjectName("modelCerceve")
        self.cerceve.setStyleSheet("""
            background-color: #303030;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin: 5px;
        """)
        
        cerceve_duzen = QVBoxLayout(self.cerceve)
        cerceve_duzen.setContentsMargins(20, 20, 20, 20)
        
        self.baslik = QLabel("AI Model")
        self.baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.baslik.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.baslik.setStyleSheet("color: #60CDFF;")
        
        self.aciklama = QLabel("Model Yüklenmemiş Durumda.")
        self.aciklama.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.aciklama.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        
        cerceve_duzen.addWidget(self.baslik)
        cerceve_duzen.addWidget(self.aciklama)
        cerceve_duzen.addStretch()
        
        self.duzen.addWidget(self.cerceve)
        
        self.animasyon_zamanlayici = QTimer(self)
        self.animasyon_zamanlayici.timeout.connect(self.dalga_animasyonu_guncelle)
        self.animasyon_zamanlayici.start(50)
        
    def giris_animasyonu_baslat(self):
        self.opak_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opak_anim.setDuration(1000)
        self.opak_anim.setStartValue(0)
        self.opak_anim.setEndValue(1)
        self.opak_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.opak_anim.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        genislik = self.width()
        yukseklik = self.height()
        orta_x = genislik / 2
        orta_y = yukseklik / 2
        
        painter.setPen(Qt.PenStyle.NoPen)
        
        dalga_sayisi = 5
        dalga_yuksekligi = 40
        
        for i in range(dalga_sayisi):
            derecelen = QLinearGradient(0, 0, genislik, 0)
            opasite = 0.05 + (0.05 * i) if not self.konusma_aktif else 0.1 + (0.05 * i)
            derecelen.setColorAt(0, QColor(0, 120, 212, int(255 * opasite)))
            derecelen.setColorAt(1, QColor(0, 213, 255, int(255 * opasite)))
            
            painter.setBrush(derecelen)
            
            yol = QPainterPath()
            yol.moveTo(0, yukseklik)
            
            ofset = i * 5
            
            for x in range(0, genislik + 10, 10):
                normallestirilmis_x = x / genislik
                dalga_faz = self.dalga_offset + ofset + (normallestirilmis_x * 2 * math.pi)
                y = orta_y + dalga_yuksekligi + (math.sin(dalga_faz) * dalga_yuksekligi)
                
                if self.konusma_aktif:
                    dalga_yuksekligi_carpan = 1.5 + math.sin(self.dalga_offset * 2) * 0.5
                    y = orta_y + dalga_yuksekligi + (math.sin(dalga_faz) * dalga_yuksekligi * dalga_yuksekligi_carpan)
                
                yol.lineTo(x, y)
            
            yol.lineTo(genislik, yukseklik)
            yol.lineTo(0, yukseklik)
            
            painter.drawPath(yol)
        
    def dalga_animasyonu_guncelle(self):
        self.dalga_offset += 0.05
        if self.dalga_offset > math.pi * 2:
            self.dalga_offset = 0
        self.update()
    
    def konusmaBaslat(self):
        self.konusma_aktif = True
        
        if hasattr(self, 'baslik'):
            self.baslik.setText("Konuşuyor...")
            self.aciklama.setText("Yanıt oluşturuluyor")
        
        if hasattr(self, 'animasyon_zamanlayici'):
            self.animasyon_zamanlayici.setInterval(25)
    
    def konusmaBitir(self):
        self.konusma_aktif = False
        
        if hasattr(self, 'baslik'):
            self.baslik.setText("AI Model")
            self.aciklama.setText("Model Yüklenmemiş Durumda.")
            
        if hasattr(self, 'animasyon_zamanlayici'):
            self.animasyon_zamanlayici.setInterval(50)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
    def showEvent(self, event):
        super().showEvent(event)
        
class ModelGorunum3D(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 480)
        self.konusma_aktif = False
        self.agiz_aciklik = 0
        self.animasyon_zamanlayici = None
        self.model_basarili = False
        
        self.kurulum()
    
    def kurulum(self):
        self.duzen = QVBoxLayout(self)
        self.duzen.setContentsMargins(0, 0, 0, 0)
        
        self.model = ModelGorunum(self)
        self.duzen.addWidget(self.model)
    
    def konusmaBaslat(self):
        self.konusma_aktif = True
        self.model.konusmaBaslat()
    
    def konusmaBitir(self):
        self.konusma_aktif = False
        self.model.konusmaBitir()
        
    def closeEvent(self, event):
        if self.animasyon_zamanlayici is not None:
            self.animasyon_zamanlayici.stop()
        super().closeEvent(event) 