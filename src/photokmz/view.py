import os
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QCheckBox ,
                             QFileDialog, QMessageBox)
from PyQt6.QtGui import QIcon
from model import Model


class VentanaPpal (QWidget):

    def __init__(self):
        super().__init__()
        self.variables_ui()
        self.inicializar_ui()


    def variables_ui(self):
        self.path_file =''
        self.list_img = []
        self.num_img = len(self.list_img)
        self.compresion = True


    def inicializar_ui(self):
        self.setFixedSize(400,150)
        self.setWindowTitle("PhotoKMZ")
        self.setWindowIcon(QIcon("./icons/photokmz.png"))
        self.widgets_ui()
        self.show()


    def widgets_ui(self):

        label_img = QLabel(self)
        label_img.setText("Seleccionar un conjunto de imágenes que contengan información gps.")
        label_img.move(10,10)

        self.label_selec = QLineEdit(self)
        self.label_selec.setText(f" {self.num_img} imágenes seleccionadas")
        self.label_selec.setReadOnly(True)
        self.label_selec.setGeometry(140,40,240,30)

        boton_seleccionar = QPushButton(self)
        boton_seleccionar.setText("SELECCIONAR")
        boton_seleccionar.resize(120,30)
        boton_seleccionar.move(20,40)
        boton_seleccionar.clicked.connect(self.seleccionar_img)

        self.check_compresion = QCheckBox(self)
        self.check_compresion.setText("Reducir y comprimir")
        self.check_compresion.setChecked(self.compresion)
        self.check_compresion.move(140,75)
        self.check_compresion.toggled.connect(self.click_compresion)

        boton_crear = QPushButton(self)
        boton_crear.setText("CREAR KMZ")
        boton_crear.resize(360,40)
        boton_crear.move(20,100)
        boton_crear.clicked.connect(self.crear_kmz)
   
    
    def seleccionar_img (self):
        dialog = QFileDialog(self)
        dialog.setDirectory(os.path.expanduser('~'))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Imágenes (*.jpeg *.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            self.list_img = dialog.selectedFiles()
            self.num_img = len(self.list_img)
            self.label_selec.setText(f" {self.num_img} imágenes seleccionadas ")
 
        
    def click_compresion(self, clicked):
        self.compresion = clicked


    def crear_kmz(self):
        if self.num_img == 0:
            QMessageBox.critical(self,"Error",
                                 "ERROR\n"
                                 "No hay imágenes seleccionadas.\n"
                                 "Por favor añada imágenes para poder crear el archivo kmz.",
                                 QMessageBox.StandardButton.Close)
        else:
            self.path_file = QFileDialog.getSaveFileName(self,"Guardar",os.path.expanduser('~'),"archivo kmz(*.kmz)")[0]
            file_name = os.path.basename(self.path_file)
            try:
                objeto_model = Model(self.list_img,
                                    self.compresion,
                                    self.path_file)
                objeto_model.crear_kmz()
                QMessageBox.information(self,"Creación finalizada",
                                        f"El archivo {file_name} se ha creado con exito !!!",
                                        QMessageBox.StandardButton.Ok,
                                        QMessageBox.StandardButton.Ok)
            except TypeError:
                QMessageBox.critical(self,"Error",
                                    "ERROR\n"
                                    "ha ocurrido un error"
                                    "Verifique las imágenes utilizadas.",
                                    QMessageBox.StandardButton.Close,
                                    QMessageBox.StandardButton.Close)
        
