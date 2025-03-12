import sys
import os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from PyQt6.QtWidgets import QApplication
    from src.main import AnaForm
    
    app = QApplication(sys.argv)
    pencere = AnaForm()
    pencere.show()
    sys.exit(app.exec()) 