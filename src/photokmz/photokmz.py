from tkinter import Tk
from view import VentanaPpal

if __name__ == '__main__':
    root_tk = Tk()
    root_tk.eval('tk::PlaceWindow . center')
    VentanaPpal(root_tk)
    
    root_tk.mainloop()