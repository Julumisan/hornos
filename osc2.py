# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 12:04:16 2023

@author: Juan Luis
"""

import pyvisa
import keyboard

# Obtener recursos VISA
rm = pyvisa.ResourceManager()
dispositivos_visa = rm.list_resources()

if len(dispositivos_visa) > 0:
    # Abrir el primer dispositivo encontrado
    with rm.open_resource(dispositivos_visa[0]) as recurso:
        recurso.timeout = 10000
        # Obtener información del dispositivo
        descripcion = recurso.query("*IDN?")  
        print("Dispositivo Visa encontrado:")
        print(f"  Descripción: {descripcion.strip()}")
        print(f"  Dirección: {dispositivos_visa[0]}")
        
        # Acciones adicionales si la descripción contiene "MSO"
        if "MSO" in descripcion:
            recurso.write("*RST")
            print("Acción adicional realizada")
            recurso.write("SELECT:CH1 ON;CH2 OFF")
            recurso.write ("HORIZONTAL:MAIN:SCALE 1E-3")
            recurso.write ("CH1:SCALE 200E-03")
           
            recurso.write(":ACQUIRE:STATE ON")
            osc = recurso
            # Obtener los voltajes del Canal 1
            
            while True:
                
                voltajes = []
                osc.write("MEASUrement:IMMed:SOUrce1 CH1")
                print(osc.write("MEASUrement:IMMed:TYPe MEAN"))
                scale = recurso.write("CH1:SCAle?")
                for i in range(20):                             
                    osc.timeout = 100000
                    voltaje = osc.query('MEASUrement:IMMed:VALue?')
                    # Agregar el número actual a la lista
                    temp = float(voltaje)
                    voltajes.append(temp)
                    
                    
                
                sol = sum(voltajes) / len(voltajes)
                
                print("Voltajes del Canal 1:", sol)
                if keyboard.is_pressed(' '):
                    break  # Salir del bucle si se ha presionado una tecla
        else:
            print("No se encontraron dispositivos Visa conectados.")



    
