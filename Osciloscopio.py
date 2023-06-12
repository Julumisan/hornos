# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 09:57:06 2023

@author: Juan Luis

Script para probar los comandos que hay que enviar al osciloscopio
"""
 
import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt


# Función para obtener los valores de voltaje del Canal 1
def obtener_voltajes_canal1(recurso):
    recurso.timeout = 100000
    osc = recurso
    
   # Configuración del osciloscopio
    osc.write('DAT:SOU CH1')  # Establecer fuente de datos al canal 1
    osc.write('DAT:ENC RPB')  # Establecer formato de datos como puntos binarios sin comprimir
    osc.write('DAT:WID 2')    # Establecer ancho de datos en 2 bytes
    osc.write('DAT:STAR 1')   # Establecer el primer punto de datos a leer
    osc.write('DAT:STOP 1000')  # Establecer el último punto de datos a leer
    osc.write('ACQ:MODE HRES')  # Establecer el modo de adquisición en alta resolución
    
    # # Configuración de la gráfica
    # plt.ion()  # Modo interactivo para actualización en tiempo real
    # plt.figure()
    
    try:
        while True:
            # Leer datos del osciloscopio
            data = osc.query_binary_values('CURV?', datatype='h', container=np.array)
    
            # Calcular el tiempo para cada punto de datos
            sample_rate = float(osc.query('ACQ:SRAT?'))
            time_per_sample = 1.0 / sample_rate
            time_values = np.arange(len(data)) * time_per_sample
            print(data)
            # Graficar los datos
            # plt.clf()
            # plt.plot(time_values, data)
            # plt.xlabel('Tiempo (s)')
            # plt.ylabel('Voltaje (V)')
            # plt.title('Lectura del Canal 1')
            # plt.grid(True)
            # plt.draw()
            # plt.pause(0.01)
    
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        # Detener la adquisición y cerrar la conexión
        osc.write('ACQ:STOPA')
        osc.close()
        rm.close()



# Obtener recursos VISA
rm = pyvisa.ResourceManager()
dispositivos_visa = rm.list_resources()

if len(dispositivos_visa) > 0:
    # Abrir el primer dispositivo encontrado
    with rm.open_resource(dispositivos_visa[0]) as recurso:
        # Obtener información del dispositivo
        descripcion = recurso.query("*IDN?")
        print("Dispositivo Visa encontrado:")
        print(f"  Descripción: {descripcion.strip()}")
        print(f"  Dirección: {dispositivos_visa[0]}")
        
        # Acciones adicionales si la descripción contiene "MSO"
        if "MSO" in descripcion:
            print("Acción adicional realizada")
            recurso.write("SELECT:CH1 ON")
            recurso.write(":ACQUIRE:STATE ON")
            
            # Obtener los voltajes del Canal 1
            voltajes = obtener_voltajes_canal1(recurso)
            print("Voltajes del Canal 1:", voltajes)
else:
    print("No se encontraron dispositivos Visa conectados.")



