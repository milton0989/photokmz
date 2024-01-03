from tkinter import StringVar, Label, Button, Tk, ttk, Checkbutton, BooleanVar
import os
from model import Model
from tkinter.filedialog import askopenfilenames, asksaveasfilename, askdirectory
from tkinter.messagebox import showinfo, showerror

BASE_DIR = os.path.dirname((os.path.abspath(__name__)))

class VentanaPpal():
    """Clase para manejar los objetos tipo ventana
    """
    def __init__(self, window ):
        self.root = window
        self.root.title("PhotoKMZ")
        self.root.attributes('-toolwindow', True)
        
               
        ### Variables
        self.list_img = StringVar()
        self.list_img = []
        self.num_img = StringVar()
        self.num_img.set('No hay imagenes seleccionadas')
        self.compresion = BooleanVar()
        self.compresion.set(True)
        self.path_file = StringVar()
                            

        # Frames
        self.input_frame = ttk.LabelFrame(self.root, text=" Imagenes ")
        self.input_frame.pack(padx=10, pady=10,fill='x', expand=True)
        
        # Etiquetas
        self.seleccion_label = Label(self.input_frame, textvariable=self.num_img, width=30)
        self.seleccion_label.grid(row=0,column=1)

        #  	Checkbutton
        self.compresion_check = Checkbutton(self.input_frame, text='Comprimir imagenes',variable=self.compresion)
        self.compresion_check.grid(row=3,column=1)

        # Boton añadir/
        self.boton_añadir = Button(self.input_frame, text = "SELECCIONAR", command = self.seleccionar,width=12)
        self.boton_añadir.grid(row=0, column=0)
        # Boton crear
        self.boton_crear = Button(self.root,text="CREAR KMZ",command=self.crear_kmz,width=12)
        self.boton_crear.pack(padx=10, pady=10, expand=False)

    

    ########## METODOS DE LA VISTA ############
    def seleccionar (self):
        self.list_img = askopenfilenames(filetypes=[("Imagenes",("*.jpg","*.jpeg"))
                                                    ,("Todos",("*.*"))]
                                                    ,initialdir=os.path.expanduser('~'))
        self.num_img.set(f"{len(self.list_img)} imagenes seleccionadas")
                

    def examinar (self):        
        self.destino.set(askdirectory(initialdir=os.path.expanduser('~')))
        if self.destino.get() == '':
            self.destino.set(os.path.expanduser('~'))
    
                 
    def crear_kmz (self):        
        if len(self.list_img) == 0 :
            showerror(message = f"No hay imagenes seleccionadas \nPor favor seleccione imagenes para poder crear el archivo kmz."
                       ,title = "Error")
        else:
            self.path_file = asksaveasfilename(defaultextension='.kmz', filetypes=[('Archivos kmz','.kmz')])
            file_name= os.path.basename(self.path_file)
            try:
                objeto_model = Model(self.list_img,
                                    self.compresion.get(),
                                    self.path_file)
                objeto_model.crear_kmz()
                showinfo(message=f"Se ha creado {file_name} de manera exitosa"
                        ,title="Creación finalizada")
            except TypeError:
                showerror(message = f"Ha ocurrido un error"
                        ,title = "Error")
        
