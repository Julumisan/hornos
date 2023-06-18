# -*- coding: utf-8 -*-
"""
Este script es un menú de elección que permite al usuario elegir entre dos opciones: "Control" y "Ver Gráfica".
Al seleccionar la opción "Control", se ejecutará el script HornoControl.py.
Al seleccionar la opción "Ver Gráfica", se abrirá una ventana de selección de archivo que permitirá al usuario
seleccionar un archivo de datos CSV.
Si se selecciona un archivo válido, se graficarán los datos contenidos en él.

Este script utiliza la biblioteca Tkinter para crear una interfaz gráfica de usuario (GUI) y para manejar eventos de usuario.

Este script contiene las siguientes funciones:
- control(): función para la opción "Control". Ejecuta el script HornoControl.py.
- ver_grafica(): función para la opción "Ver Gráfica". Abre una ventana de selección de archivo y, si se selecciona un archivo válido, grafica los datos contenidos en él.
- salir(): función para la opción "Salir". Cierra la ventana principal y sale del script.

Además, contiene una variable global "imagen_icono" que almacena una imagen que se muestra en el botón "Ver Gráfica".
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import graficar
from HornoControl import HornoControl
import sys

imagen_icono = None


def control():

    """
    Función para la opción "Control".
    Ejecuta el script HornoControl.py utilizando la biblioteca subprocess.
    """
    print("Soy el control")
    subprocess.run(['python', 'HornoControl.py'])
    


def ver_grafica():

    """
    Función para la opción "Ver Gráfica".
    Abre una ventana de selección de archivo que permite al usuario seleccionar un archivo de datos CSV.
    Si se selecciona un archivo válido, grafica los datos contenidos en él utilizando la función leer_datos_csv de la biblioteca graficar.
    Además, carga una imagen "icono.png" que se muestra en el botón "Ver Gráfica".
    """
    global imagen_icono
    print("Soy una grafica")
    archivo_datos = filedialog.askopenfilename(title="Seleccionar archivo de datos",
    filetypes=(("CSV files", ".csv"),
    ("all files", ".*")))
    print("Archivo de datos:", archivo_datos)
    if archivo_datos:
        graficar.leer_datos_csv(archivo_datos)
        # imagen_icono = None
    else:
        tk.messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
        # imagen_icono = tk.PhotoImage(file="icono.png")
        # boton_ver_grafica.config(image=imagen_icono, compound="left")

def salir():

    """
    Función para la opción "Salir".
    Cierra la ventana principal y sale del script utilizando la función sys.exit().
    """
    if messagebox.askokcancel("Salir", "¿Desea salir?"):
        ventana.destroy()
        sys.exit()
        
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Menú Principal")
ventana.geometry("180x225")  # tamaño y posición de la ventana
ventana.configure(bg="#EFEFEF")  # color de fondo

# Crear botones
boton_control = tk.Button(ventana, text="Control", font=("Arial", 14), bg="lightgray", command=control)
boton_ver_grafica = tk.Button(ventana, text="Ver Gráfica", font=("Arial", 14), bg="lightgray", command=ver_grafica)
boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 14), bg="lightgray", command=salir)


# Colocar botones en la ventana
boton_control.place(relx=0.5, rely=0.3, anchor="center")
boton_ver_grafica.place(relx=0.5, rely=0.5, anchor="center")
boton_salir.place(relx=0.5, rely=0.7, anchor="center")

# Iniciar bucle de la ventana
ventana.mainloop()
ventana.protocol("WM_DELETE_WINDOW", salir)
