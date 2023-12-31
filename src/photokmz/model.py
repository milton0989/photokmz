import os
import zipfile
import shutil
from PIL import Image
import tempfile
from pathlib import Path
import simplekml
from gpsexif import image_lon, image_lat


class Model:
    
    def __init__(self, list_img, compresion, destino, nombre_kmz):
        self.list_img = list_img      # lista de imagenes a procesar
        self.compresion = compresion  # variable para comprimimir imagen
        self.destino = destino        # directorio de destino para el archivo
        self.nombre_kmz = nombre_kmz  # nombre del archivo kmz


    def crear_kmz(self):
        dir_temp = tempfile.TemporaryDirectory()  #dir=os.getcwd()creo un directorio temporal en la direccion dir=OPCIONAL (depende S.O.)
        path_temp = Path(dir_temp.name) # tranformar str a path
        
        dir_img = os.path.join(path_temp,"img") # Creo la ruta (str) para el directorio img
        path_img = Path(dir_img)    # tranformo str a path
        os.mkdir(path_img)  # Creo el directorio '/img' dentro del directorio temporal

        self._copiar_img(path_img)        
        if self.compresion == True:
            self._comprimir_imagenes(path_img)        
        self._crear_kml(path_temp, path_img)
        self._comprimir_directorio(path_temp)

        os.chdir(self.destino) # establecer puntero en directorio destino para evitar error de recursividad
        #input("Pulse enter para finalizar: ") # solo para probar
             
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
        
    def _crear_kml (self, ruta_tmp, ruta_img_tmp):
        os.chdir(ruta_tmp)  # me coloco en el directorio tmp
        kml = simplekml.Kml()

      
        for file in os.listdir(ruta_img_tmp):            
            longitud = image_lon(f"./img/{os.path.relpath(file)}")
            latitud = image_lat(f"./img/{os.path.relpath(file)}")
            punto = kml.newpoint(name=os.path.relpath(file),
                                coords=[(longitud,latitud)],
                                description=f"""<BR><img style="max-width:500px;max-height:500px" src="img/{os.path.relpath(file)}"></img><BR>""",)  #{file} lon, lat, optional height
            punto.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        
        kml.save("imagenes.kml")
        
        print('se ha creado el kml')
    
            
            
             

    def _comprimir_directorio(self, ruta_tmp):        

        mi_zip = zipfile.ZipFile(os.path.join(self.destino,f'{self.nombre_kmz}.kmz'), 'w')

        for folder, subfolders, files in os.walk(ruta_tmp):
            for file in files:
                mi_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), ruta_tmp), compress_type = zipfile.ZIP_DEFLATED)

        mi_zip.close()
              
        print('se ha comprimido en kmz')
        
        
    

if __name__ == '__main__':
    imagenes_prueba = ('C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142826317_HDR.jpg', 
                    'C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142959656.jpg', 
                    'C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_143007828.jpg',
                        'C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_143039395_HDR.jpg')   

    instancia_modelo = Model(imagenes_prueba,True,os.getcwd(),'nombre' )
    instancia_modelo.crear_kmz()

