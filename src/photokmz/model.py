import os
import shutil
from PIL import Image
import tempfile
import simplekml
from gpsexif import image_lon, image_lat


class Model:
    
    def __init__(self, list_img, compresion, path_kmz):
        self.list_img = list_img      # lista de imagenes a procesar
        self.compresion = compresion  # variable para comprimimir imagen
        self.path_kmz = path_kmz      # ruta del archivo kmz


    def crear_kmz(self):
        
        if self.compresion == True:
            dir_temp = tempfile.TemporaryDirectory()  #creo un directorio temporal en la direccion dir=OPCIONAL (depende S.O.)
            path_temp = dir_temp.name
            self._copiar_img(path_temp)   
            self._comprimir_imagenes(path_temp)
            self.list_img = [os.path.join(path_temp,file) for file in os.listdir(path_temp) ]
            os.chdir(os.path.expanduser('~')) # cambio de directorio para no tener error de recursividad
        
        kml = simplekml.Kml()
        for file in self.list_img:
            file_name = os.path.basename(file)
            try:
                longitud = image_lon(file)
                latitud = image_lat(file)
            except:
                longitud, latitud = (None, None)
            if longitud: #Se añade al kml unicamente si tiene valor de Longitud.
                point = kml.newpoint(name = file_name , coords = [(longitud,latitud)])
                picpath = kml.addfile(file)
                point.description = '<img style="max-width:500px;max-height:500px" src="' + picpath +'" />'
                point.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

        kml.savekmz(self.path_kmz, format = False)

        mensaje = f"Se ha creado el KMZ con exito!!"
        return mensaje
        
    
    def _copiar_img (self, ruta_img_temp):
        for imagen in self.list_img:
            #print(ruta_img_temp)
            shutil.copy(imagen,ruta_img_temp)                   
        print('se han copiado las imagenes')


    def _comprimir_imagenes(self, ruta_img_temp):
        os.chdir(ruta_img_temp)  # me coloco en el directorio de las imagenes
        #print(os.getcwd())  #imprime el directorio donde me encuentro
        for imagen in os.listdir(ruta_img_temp):
            img_orig = Image.open(imagen)
            exif = img_orig.getexif()
            img_orig.thumbnail((800,800))
            img_orig.save(imagen, exif=exif)
        print("se han comprimido las imagenes")
        
