from cx_Freeze import setup, Executable
import sys
import os

build_options = {'packages': [],
                 'excludes': [],
                 'include_files':['LICENSE','README.md',]}


base = 'Win32GUI' if sys.platform=='win32' else None


ruta_relativa = "src/photokmz"
ruta_absoluta = os.path.abspath(ruta_relativa) #convierto en ruta absoluta
sys.path.append(ruta_absoluta) # la agrego al sys.path para que python encuentre los modulos

executables = [
    Executable(os.path.join(ruta_absoluta, 'photokmz.py'),
               base=base,
               target_name = 'photokmz',
               icon='src/photokmz/icono.ico',
               shortcut_name="PhotoKMZ",
               shortcut_dir="ProgramMenuFolder") #"DesktopFolder"
]

setup(name='PhotoKMZ',
      version = '0.1.0',
      description = 'Crea kmz a partir de fotografias',
      options = {'build_exe': build_options},
      author = 'Milton Villar',
      executables = executables)
