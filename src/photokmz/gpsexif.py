"""
gpsexif.py
Modulo con funciones para extraer coordenadadas GPS de un archivo imagen.
Adaptado de https://keithmfoster.com/image-file-metadata-and-python/
"""
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif_data(image_path):
    """Extract EXIF metadata from the image file."""
    with Image.open(image_path) as img:
        # Get the raw EXIF data
        exif_data = img._getexif()
        if not exif_data:
            return None
 
        # Convert the raw EXIF data into a dictionary of human-readable tags
        exif_tags = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'GPSInfo':
                value = get_gps_info(value)
            exif_tags[tag] = value
 
        return exif_tags
 
def get_gps_info(gps_info):
    """Convert raw GPS metadata into a dictionary of human-readable tags."""
    gps_tags = {}
    for tag_id, value in gps_info.items():
        tag = GPSTAGS.get(tag_id, tag_id)
        gps_tags[tag] = value
    return gps_tags
 
def get_gps_data(exif_data):
    """Extract the latitude and longitude data from the GPS metadata."""
    gps_info = exif_data.get('GPSInfo')
    if not gps_info:
        return None
 
    latitude = convert_gps_coords(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
    longitude = convert_gps_coords(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
 
    return latitude, longitude
 
def convert_gps_coords(coords, ref):
    """Convert GPS coordinates from (degrees, minutes, seconds) format to decimal format."""
    decimal_coords = float(coords[0]) + (float(coords[1]) / 60) + (float(coords[2]) / 3600)
    if ref in ('S', 'W'):
        decimal_coords = -decimal_coords
    return decimal_coords
 
def decimal_degrees_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    decimal_minutes = abs(decimal_degrees - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = (decimal_minutes - minutes) * 60
    return degrees, minutes, seconds

def image_lat(image_path, formato='decimal'):
    """Función que retorna la latitud de un archivo imagen.
        
        :param image_path: la ruta del archivo imagen.
        :type image_path: str
        :param formato: el formato en que se presentara la latitud, puede ser 'decimal' 
            o 'dms' (grados-minutos-segundos), por defecto es 'decimal'
        :type: formato: str, optional

        :return: La longitud geografica de la imagen
        :rtype: str        
    
    """

    exif_data = get_exif_data(image_path)
    if exif_data:
        latitude, longitude = get_gps_data(exif_data)
        if formato == 'decimal':            
            return latitude
        if formato == 'dms':  
            degrees, minutes, seconds,  = decimal_degrees_to_dms(latitude)
            return f"Latitude: {degrees}° {minutes}' {seconds:.2f}\""
    else:
        raise TypeError('No se encontraron metadatos EXIF ​​en el archivo de imagen.')

def image_lon(image_path, formato='decimal'):
    """Función que retorna la longitud de un archivo imagen.
        
        :param image_path: la ruta del archivo imagen.
        :type image_path: str
        :param formato: el formato en que se presentara la latitud, puede ser 'decimal' 
            o 'dms' (grados-minutos-segundos), por defecto es 'decimal'
        :type: formato: str, optional

        :return: La longitud geografica de la imagen.
        :rtype: str        
    
    """
    exif_data = get_exif_data(image_path)
    if exif_data:
        latitude, longitude = get_gps_data(exif_data)
        if formato == 'decimal':            
            return longitude
        if formato == 'dms':  
            degrees, minutes, seconds,  = decimal_degrees_to_dms(longitude)
            return f"Latitude: {degrees}° {minutes}' {seconds:.2f}\""
    else:
        raise TypeError('No se encontraron metadatos EXIF ​​en el archivo de imagen.')
 
if __name__ == '__main__':
    #use any jpg image.
    image_path = 'C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142826317_HDR.jpg'
    exif_data = get_exif_data(image_path)
    if exif_data:
        date_taken = exif_data.get('DateTimeOriginal')
        latitude, longitude = get_gps_data(exif_data)
        print(f'Date taken: {date_taken}')
        print(f'Latitude: {latitude}')
        degrees, minutes, seconds,  = decimal_degrees_to_dms(latitude)
        print(f"Latitude: {degrees}° {minutes}' {seconds:.2f}\"")
        print(f'Longitude: {longitude}')
        degrees, minutes, seconds = decimal_degrees_to_dms(longitude)
        print(f"Longitude: {degrees}° {minutes}' {seconds:.2f}\"")
    else:
        print('No EXIF metadata found in image file.')

    print(image_lat('C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142826317_HDR.jpg'))
    print(type(image_lat('C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142826317_HDR.jpg')))
    print(image_lon('C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142826317_HDR.jpg', 'dms'))
    print(type(image_lon('C:/Users/joha_/Desktop/PruebaOpenFile/imagenes_test/IMG_20200729_142826317_HDR.jpg', 'dms')))
        