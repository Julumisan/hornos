# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:29:59 2023

@author: Julu
"""

import csv
import matplotlib.pyplot as plt
# import sys



def leer_datos_csv(nombre_archivo):
    
    # Abrir el archivo con el nombre especificado en modo lectura ('r')
    # El archivo se cierra automáticamente al salir del bloque 'with'
    with open(nombre_archivo, 'r') as file:
        # Crear un objeto 'reader' de la clase csv.reader
        # El objeto 'reader' permite leer los datos del archivo CSV línea por línea
        reader = csv.reader(file)
        
        # Obtener la primera línea del archivo (los encabezados)
        # La función next() devuelve la siguiente línea del objeto 'reader'
        header = next(reader)
        
        # Leer los datos del archivo CSV a una lista
        # La función list() convierte el objeto 'reader' a una lista de listas
        # Cada lista interna contiene los valores de cada fila del archivo CSV
        data = list(reader)
    
    print("He entrado") 
    # Convertir datos a listas
    tiempo = [float(row[0]) for row in data]
    temperatura = [float(row[1]) for row in data]
    temp_max = [float(row[2]) for row in data]
    temp_min = [float(row[3]) for row in data]
     
    # Crear gráfica
    plt.plot(tiempo, temperatura, label="Temperatura")
    plt.plot(tiempo, temp_max, label="Temp. Máx")
    plt.plot(tiempo, temp_min, label="Temp. Mín")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.show()
       

# Conseguir el nombre de archivo con el subprocess desde menu
# nombre_archivo = sys.argv[1] 
# leer_datos_csv(nombre_archivo)
