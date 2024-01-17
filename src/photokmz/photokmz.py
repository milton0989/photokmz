import sys
from PyQt6.QtWidgets import QApplication
from view import VentanaPpal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPpal()
    sys.exit(app.exec())
