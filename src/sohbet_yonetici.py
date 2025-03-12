from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QWidget, QFrame, QLabel, QLineEdit, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QTimer, QParallelAnimationGroup
from PyQt6.QtGui import QIcon, QFont, QColor, QAction, QPixmap, QCursor
import json
import os
from datetime import datetime

class SohbetButonu(QPushButton):
    silSignal = pyqtSignal(str)
    yenidenAdlandirSignal = pyqtSignal(str)
    
    def __init__(self, sohbet_id, baslik, parent=None):
        super().__init__(parent)
        self.sohbet_id = sohbet_id
        self.baslik = baslik
        self.setUp()
        
    def setUp(self):
        self.setText(self.baslik)
        self.setCheckable(True)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(50)
        self.setMinimumWidth(150)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 16px;
                border-radius: 8px;
                border: none;
                background-color: rgba(0, 0, 0, 0.1);
                color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
                color: white;
            }
            QPushButton:checked {
                background-color: rgba(0, 120, 212, 0.5);
                color: white;
            }
        """)
        
        duzen = QHBoxLayout(self)
        duzen.setContentsMargins(0, 0, 8, 0)
        duzen.setSpacing(8)
        
        duzen.addStretch()
        
        self.duzenleButton = QPushButton("", self)
        self.duzenleButton.setObjectName("duzenleButton")
        self.duzenleButton.setIcon(QIcon("src/model/duzenle_ikonu.png"))
        self.duzenleButton.setFixedSize(32, 32)
        self.duzenleButton.setIconSize(QSize(16, 16))
        self.duzenleButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.duzenleButton.setToolTip("Sohbeti Yeniden Adlandır")
        self.duzenleButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 0.15);
            }
        """)
        self.duzenleButton.clicked.connect(self.yenidenAdlandir)
        duzen.addWidget(self.duzenleButton)
        
        self.silButton = QPushButton("", self)
        self.silButton.setObjectName("silButton")
        self.silButton.setIcon(QIcon("src/model/sil_ikonu.png"))
        self.silButton.setFixedSize(32, 32)
        self.silButton.setIconSize(QSize(16, 16))
        self.silButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.silButton.setToolTip("Sohbeti Sil")
        self.silButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.15);
            }
        """)
        self.silButton.clicked.connect(self.sohbetiSil)
        duzen.addWidget(self.silButton)
        
        self.setFixedHeight(50)
        for buton, dosya in [(self.duzenleButton, "src/model/duzenle_ikonu.png"), 
                           (self.silButton, "src/model/sil_ikonu.png")]:
            if not os.path.exists(dosya) or os.path.getsize(dosya) < 100:
                if "duzenle" in dosya:
                    buton.setText("✏️")
                    buton.setIcon(QIcon())
                elif "sil" in dosya:
                    buton.setText("🗑️")
                    buton.setIcon(QIcon())
                    
    def yenidenAdlandir(self):
        self.yenidenAdlandirSignal.emit(self.sohbet_id)
        
    def sohbetiSil(self):
        self.silSignal.emit(self.sohbet_id)
        
    def setText(self, text):
        self.baslik = text
        super().setText(text)

class SohbetYonetici(QFrame):
    sohbetDegisti = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sohbetYonetici")
        self.setMinimumWidth(250)
        self.setMaximumWidth(350)
        
        self.sohbetler = {}
        self.aktif_sohbet_id = None
        self.gpt_baglanti = None
        self.daraltildi = False
        
        self.buton_stil = """
            QPushButton {
                text-align: left;
                padding-left: 16px;
                border-radius: 8px;
                border: none;
                background-color: rgba(0, 0, 0, 0.1);
                color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.2);
                color: white;
            }
        """
        
        self.secili_buton_stil = """
            QPushButton {
                text-align: left;
                padding-left: 16px;
                border-radius: 8px;
                border: none;
                background-color: rgba(0, 120, 212, 0.5);
                color: white;
            }
        """
        
        self.kurulum()
        
    def kurulum(self):
        self.setStyleSheet("""
            QFrame#sohbetYonetici {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            QPushButton#yeniSohbetButton {
                background-color: rgba(0, 120, 212, 0.7);
                color: white;
                border-radius: 8px;
                padding: 8px;
                text-align: center;
                font-weight: bold;
            }
            
            QPushButton#yeniSohbetButton:hover {
                background-color: rgba(0, 120, 212, 1.0);
            }
            
            QPushButton#daraltButon {
                background-color: transparent;
                border-radius: 16px;
            }
            
            QPushButton#daraltButon:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        
        self.duzen = QVBoxLayout(self)
        self.duzen.setContentsMargins(8, 16, 8, 16)
        self.duzen.setSpacing(8)
        
        ust_duzen = QHBoxLayout()
        ust_duzen.setContentsMargins(8, 0, 8, 8)
        
        baslik = QLabel("Sohbetler", self)
        baslik.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        baslik.setStyleSheet("color: white;")
        ust_duzen.addWidget(baslik)
        
        ust_duzen.addStretch()
        
        self.daraltButon = QPushButton("", self)
        self.daraltButon.setObjectName("daraltButon")
        self.daraltButon.setIcon(QIcon("src/model/daralt_ikonu.png"))
        self.daraltButon.setFixedSize(32, 32)
        self.daraltButon.setIconSize(QSize(16, 16))
        self.daraltButon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.daraltButon.setToolTip("Panel Daralt")
        self.daraltButon.clicked.connect(self.daralt_genislet)
        ust_duzen.addWidget(self.daraltButon)
        
        self.duzen.addLayout(ust_duzen)
        
        self.yeniSohbetButton = QPushButton("+ Yeni Sohbet", self)
        self.yeniSohbetButton.setObjectName("yeniSohbetButton")
        self.yeniSohbetButton.setFixedHeight(40)
        self.yeniSohbetButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.yeniSohbetButton.clicked.connect(self.yeniSohbet)
        self.duzen.addWidget(self.yeniSohbetButton)
        
        self.liste_alani = QScrollArea(self)
        self.liste_alani.setWidgetResizable(True)
        self.liste_alani.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.liste_alani.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.liste_container = QWidget(self.liste_alani)
        self.liste_container.setStyleSheet("background-color: transparent;")
        
        self.liste_duzen = QVBoxLayout(self.liste_container)
        self.liste_duzen.setContentsMargins(0, 8, 0, 8)
        self.liste_duzen.setSpacing(8)
        self.liste_duzen.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.liste_alani.setWidget(self.liste_container)
        self.duzen.addWidget(self.liste_alani, 1)
    
    def set_gpt_baglanti(self, baglanti):
        self.gpt_baglanti = baglanti
        self.sohbet_listesini_guncelle()
    
    def sohbet_listesini_guncelle(self):
        try:
            if not self.gpt_baglanti:
                return
                
            for i in reversed(range(self.liste_duzen.count())):
                widget = self.liste_duzen.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            
            self.sohbetler = {}
            
            for sohbet in self.gpt_baglanti.sohbet_listesi:
                self.sohbet_buton_ekle(sohbet["id"], sohbet["baslik"])
                
            if self.gpt_baglanti.aktif_sohbet_id:
                self.aktif_sohbet_id = self.gpt_baglanti.aktif_sohbet_id
                if self.aktif_sohbet_id in self.sohbetler:
                    self.sohbetler[self.aktif_sohbet_id].setChecked(True)
        except Exception as e:
            print(f"Sohbet listesi güncelleme hatası: {str(e)}")
    
    def yeniSohbet(self):
        if not self.gpt_baglanti:
            return
            
        try:
            maksimum_sohbet = 10
            
            if len(self.sohbetler) >= maksimum_sohbet:
                QMessageBox.warning(self, "Sohbet Limiti", f"Maksimum {maksimum_sohbet} sohbet oluşturabilirsiniz. Yeni sohbet açmak için eski sohbetleri silin.")
                return
                
            sohbet_id = self.gpt_baglanti.yeniSohbetBaslat()
            
            if sohbet_id:
                baslik = f"Yeni Sohbet {len(self.sohbetler) + 1}"
                self.sohbet_buton_ekle(sohbet_id, baslik)
                self.sohbetSec(sohbet_id)
            else:
                QMessageBox.warning(self, "Hata", "Yeni sohbet başlatılamadı.")
        except Exception as e:
            print(f"Yeni sohbet hatası: {str(e)}")
    
    def sohbetSec(self, sohbet_id):
        if not sohbet_id or sohbet_id not in self.sohbetler:
            return
        
        for s_id, buton in self.sohbetler.items():
            if isinstance(buton, dict):
                continue
                
            if s_id == sohbet_id:
                buton.setChecked(True)
                buton.setStyleSheet(self.secili_buton_stil)
            else:
                buton.setChecked(False)
                buton.setStyleSheet(self.buton_stil)
        
        self.aktif_sohbet_id = sohbet_id
        
        if self.gpt_baglanti:
            self.gpt_baglanti.sohbet_sec(sohbet_id)
            
        self.sohbetDegisti.emit(sohbet_id)
    
    def sohbetiSil(self, sohbet_id):
        if not self.gpt_baglanti or sohbet_id not in self.sohbetler:
            return
            
        onay = QMessageBox.question(self, "Sohbet Silme", "Bu sohbeti silmek istediğinize emin misiniz?")
        
        if onay == QMessageBox.StandardButton.Yes:
            try:
                if self.gpt_baglanti.sohbet_sil(sohbet_id):
                    if sohbet_id in self.sohbetler:
                        self.sohbetler[sohbet_id].setParent(None)
                        del self.sohbetler[sohbet_id]
                        
                    if sohbet_id == self.aktif_sohbet_id:
                        self.aktif_sohbet_id = None
                        if self.sohbetler:
                            ilk_sohbet_id = list(self.sohbetler.keys())[0]
                            self.sohbetSec(ilk_sohbet_id)
                        else:
                            self.sohbetDegisti.emit("")
            except Exception as e:
                QMessageBox.warning(self, "Sohbet Silme Hatası", f"Sohbet silinirken hata: {str(e)}")
    
    def sohbetiYenidenAdlandir(self, sohbet_id):
        if not self.gpt_baglanti or sohbet_id not in self.sohbetler:
            return
        
        mevcut_baslik = self.sohbetler[sohbet_id]["baslik"] if isinstance(self.sohbetler[sohbet_id], dict) else self.sohbetler[sohbet_id].baslik

        dialog = QMessageBox(self)
        dialog.setWindowTitle("Sohbeti Yeniden Adlandır")
        dialog.setText("Sohbet için yeni başlık girin:")

        line_edit = QLineEdit(dialog)
        line_edit.setText(mevcut_baslik)
        line_edit.setFixedWidth(300)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Yeni Başlık:"))
        layout.addWidget(line_edit)
        
        content = QWidget()
        content.setLayout(layout)
        
        dialog.layout().addWidget(content, 1, 0, 1, dialog.layout().columnCount())
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if dialog.exec() == QMessageBox.StandardButton.Ok:
            yeni_baslik = line_edit.text().strip()
            if yeni_baslik:
                try:
                    if self.gpt_baglanti:
                        self.gpt_baglanti.sohbet_yeniden_adlandir(sohbet_id, yeni_baslik)
                    
                    if sohbet_id in self.sohbetler:
                        if isinstance(self.sohbetler[sohbet_id], dict):
                            self.sohbetler[sohbet_id]["baslik"] = yeni_baslik
                        else:
                            self.sohbetler[sohbet_id].setText(yeni_baslik)
                except Exception as e:
                    QMessageBox.warning(self, "Yeniden Adlandırma Hatası", f"Sohbet yeniden adlandırılırken hata: {e}")
    
    def daralt_genislet(self):
        if self.daraltildi:
            genisletme_anim = QPropertyAnimation(self, b"minimumWidth")
            genisletme_anim.setDuration(300)
            genisletme_anim.setStartValue(50)
            genisletme_anim.setEndValue(250)
            genisletme_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            maksimum_anim = QPropertyAnimation(self, b"maximumWidth")
            maksimum_anim.setDuration(300)
            maksimum_anim.setStartValue(50)
            maksimum_anim.setEndValue(350)
            maksimum_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            grup = QParallelAnimationGroup(self)
            grup.addAnimation(genisletme_anim)
            grup.addAnimation(maksimum_anim)
            
            self.daraltButon.setIcon(QIcon("src/model/daralt_ikonu.png"))
            self.daraltButon.setToolTip("Panel Daralt")
            
            self.goster_sohbet_liste(True)
            grup.start()
            
            self.daraltildi = False
        else:
            daraltma_anim = QPropertyAnimation(self, b"minimumWidth")
            daraltma_anim.setDuration(300)
            daraltma_anim.setStartValue(250)
            daraltma_anim.setEndValue(50)
            daraltma_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            maksimum_anim = QPropertyAnimation(self, b"maximumWidth")
            maksimum_anim.setDuration(300)
            maksimum_anim.setStartValue(350)
            maksimum_anim.setEndValue(50)
            maksimum_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            grup = QParallelAnimationGroup(self)
            grup.addAnimation(daraltma_anim)
            grup.addAnimation(maksimum_anim)
            
            self.daraltButon.setIcon(QIcon("src/model/genislet_ikonu.png"))
            self.daraltButon.setToolTip("Panel Genişlet")
            
            grup.start()
            grup.finished.connect(lambda: self.goster_sohbet_liste(False))
            
            self.daraltildi = True
    
    def goster_sohbet_liste(self, goster):
        self.yeniSohbetButton.setVisible(goster)
        self.liste_alani.setVisible(goster)
        
        for widget in [self.duzen.itemAt(0).layout().itemAt(0).widget()]:
            if widget:
                widget.setVisible(goster)
    
    def mesaj_ekle(self, metin, gonderici):
        if not self.aktif_sohbet_id or not self.gpt_baglanti:
            return
            
        try:
            if gonderici == "kullanici":
                self.gpt_baglanti.mesaj_gonder(metin)
        except Exception as e:
            print(f"Mesaj ekleme hatası: {str(e)}")
    
    def sohbet_buton_ekle(self, sohbet_id, baslik):
        if not sohbet_id or not baslik:
            return
            
        buton = SohbetButonu(sohbet_id, baslik, self.liste_container)
        buton.clicked.connect(lambda: self.sohbetSec(sohbet_id))
        buton.silSignal.connect(self.sohbetiSil)
        buton.yenidenAdlandirSignal.connect(self.sohbetiYenidenAdlandir)
        
        self.liste_duzen.addWidget(buton)
        self.sohbetler[sohbet_id] = buton
    
    def aktif_sohbet_mesajlari(self):
        if not self.aktif_sohbet_id or not self.gpt_baglanti:
            return []
            
        return self.gpt_baglanti.get_sohbet_mesajlari(self.aktif_sohbet_id)
    
    def tema_degistir(self, tema_adi, renkler=None):
        if not renkler:
            return
            
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {renkler['panel']};
                color: {renkler['metin']};
            }}
            QPushButton {{
                background-color: {renkler['buton']};
                border-radius: 8px;
                color: {renkler['metin']};
                padding: 6px;
            }}
            QPushButton:hover {{
                background-color: {renkler['buton_hover']};
            }}
            QPushButton:pressed {{
                background-color: {renkler['buton_aktif']};
                color: white;
            }}
            QLineEdit {{
                background-color: {renkler['panel_sekonder']};
                border-radius: 8px;
                color: {renkler['metin']};
                border: 1px solid {renkler['kenar']};
                padding: 8px;
            }}
            QScrollArea {{
                background-color: {renkler['panel']};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {renkler['panel']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {renkler['kenar']};
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
        
        for sohbet in self.sohbetler.values():
            if hasattr(sohbet, "setProperty"):
                sohbet.setProperty("tema", tema_adi)
                sohbet.style().unpolish(sohbet)
                sohbet.style().polish(sohbet)
                
        if hasattr(self, 'daraltButon'):
            self.daraltButon.setStyleSheet(f"""
                QPushButton {{
                    background-color: {renkler['buton']};
                    border-radius: 16px;
                }}
                QPushButton:hover {{
                    background-color: {renkler['buton_hover']};
                }}
            """)

    def panel_daralt_genislet_durumu(self, daraltildi):
        self.setVisible(not daraltildi)
        if hasattr(self, 'yeniSohbetButton'):
            self.yeniSohbetButton.setVisible(not daraltildi)
        
        if hasattr(self, 'sohbetPanel'):
            self.sohbetPanel.setVisible(not daraltildi)