# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:22:07 2023

@author: Julu

La idea de este Script es que sea el menú de elección.

"""

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import graficar
import sys


def control():
    # función para la opción "Control"
    print("Soy el control")
    subprocess.run(['python', 'Horno_v3.0.py'])
    
def ver_grafica():
    # función para la opción "Ver Gráfica"
    print("Soy una grafica")
    archivo_datos = filedialog.askopenfilename(title="Seleccionar archivo de datos",
                                               filetypes=(("CSV files", "*.csv"),
                                                          ("all files", "*.*")))
    print("Archivo de datos:", archivo_datos)
    if archivo_datos:
        graficar.leer_datos_csv(archivo_datos)
    else:
        tk.messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
        
    
def salir():
    if messagebox.askokcancel("Salir", "¿Desea salir?"):
        ventana.destroy()
        sys.exit()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Menú Principal")

# Crear botones
boton_control = tk.Button(ventana, text="Control", command=control)
boton_ver_grafica = tk.Button(ventana, text="Ver Gráfica", command=ver_grafica)
boton_salir = tk.Button(ventana, text="Salir", command=salir)

# Colocar botones en la ventana
boton_control.pack(padx=50, pady=10)
boton_ver_grafica.pack(padx=50, pady=10)
boton_salir.pack(padx=50, pady=10)

# Iniciar bucle de la ventana
ventana.mainloop()
ventana.protocol("WM_DELETE_WINDOW", salir)