# PhotoKMZ
Herramienta gráfica para crear un archivo kmz a partir de imágenes con información gps.

<center><img src="./capturas/image.png"></center>
<center><img src="./capturas/captura_02.png"></center>

## Características
- Se utiliza [Pillow](https://pypi.org/project/pillow/) para obtener las coordenadas a partir los metadatos exif de cada imagen.
- Se puede reducir y comprimir las imágenes para disminuir el tamaño del archivo kmz.
- Se utiliza [simplekml](https://pypi.org/project/simplekml/) para generar el archivo kmz.

## Instalación
### Utilizando python
- Clonar este repositorio.
- Instalar Python >= 3.9.7
- Instalar las dependencias utilizando: <pre><code>pip install -r requirements.txt
</code></pre>
- Ejecutar el script photokmz.py

### Ejecutables
Para obtener ejecutables se utiliza [cx_Freeze](https://pypi.org/project/cx-Freeze/) :
<pre><code>python setup.py build</code></pre>
- En Windows se puede generar un instalador .msi con: <pre><code>python setup.py bdist_msi</code></pre>
- Puede descargar instaladores [AQUÍ](https://github.com/milton0989/photokmz/releases) 