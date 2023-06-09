# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 09:57:06 2023

@author: Juan Luis

Script para probar los comandos que hay que enviar al osciloscopio
"""
 
import pyvisa

# Función para obtener los valores de voltaje del Canal 1
def obtener_voltajes_canal1(recurso):
    recurso.timeout = 100000
    oscilloscope = recurso
    
    # Query the vertical scale and offset
    # vertical_scale = float(oscilloscope.query("CH1:SCALE?"))
    vertical_offset = float(oscilloscope.query("CH1:OFFSET?"))
    vertical_divisions = float(oscilloscope.query("CH1:SCALE?"))
    print (vertical_divisions)
    
    # Query the horizontal scale and offset
    horizontal_scale = float(oscilloscope.query("HORIZONTAL:SCALE?"))
    horizontal_offset = float(oscilloscope.query("HORIZONTAL:POSITION?"))
    
    # Set up the acquisition parameters
    oscilloscope.write("DATA:SOURCE CH1")  # Select the desired channel
    oscilloscope.write("DATA:ENCdg ASCII")  # Set the data encoding to ASCII
    oscilloscope.write("DATA:WIDTH 1")  # Set the data width to 1 byte per point
    
    # Read the waveform data
    waveform_data = oscilloscope.query_ascii_values("CURVE?")
    print(waveform_data)
    
    # Calculate voltage per division and voltages
    voltage_per_division = vertical_divisions
    voltages = [(v * voltage_per_division) - vertical_offset for v in waveform_data]
    
    # Calculate time values
    time_values = [(i * horizontal_scale) - horizontal_offset for i in range(len(waveform_data))]
    
    # Close the connection
    oscilloscope.close()
    rm.close()
    
    # Print the first 10 voltage and time values
    print("Voltage (V):", voltages[:10])
    print("Time (s):", time_values[:10])
    
    
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


