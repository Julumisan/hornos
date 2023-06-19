# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 12:04:16 2023

@author: Juan Luis
"""

import pyvisa
import time
# Obtener recursos VISA
try:
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
                recurso.write ("HORIZONTAL:MAIN:SCALE 1E-3")
                recurso.write ("CH1:SCALE 100E-03")
                recurso.write ("CH2:SCALE 100E-03")
                recurso.write ("CH1:POSition -3")
                recurso.write ("CH2:POSition -3")     
                recurso.write("MEASUrement:MEAS1:STATE ON")
                recurso.write("MEASUrement:MEAS1:SOURCE CH1")
                recurso.write("MEASUrement:MEAS1:TYPe MEAN")
                recurso.write("MEASUrement:MEAS2:STATE ON")
                recurso.write("MEASUrement:MEAS2:SOURCE CH2")
                recurso.write("MEASUrement:MEAS2:TYPe MEAN")
                recurso.write("MEASUrement:MEAS3:STATE ON")
                recurso.write("MEASUrement:MEAS3:SOURCE MATH1")
                recurso.write("MEASUrement:MEAS3:TYPe MEAN")
                recurso.write("SELECT:CH1 ON;CH2 ON")
                recurso.write("MATH1:DEFINE \"CH1-CH2\"")
                recurso.write("SELECT:MATH1 ON")  
                recurso.write ("MATH1:VERTICAL:POSition -3")
                recurso.write ("MATH1:SCALE 100E-03")
                time.sleep(1)

                
                # recurso.write(":ACQUIRE:STATE ON")

               

                osc = recurso
                # Obtener los voltajes del Canal 1
                
                while True:
                    
                    voltajes = []
                    # osc.write("MEASUrement:IMMed:SOUrce1 MATH1")
                    print(osc.write("MEASUrement:IMMed:TYPe MEAN"))
                    # print(osc.write("MEASUrement:IMMed:TYPe AMPlitude"))
                    scale = recurso.write("CH1:SCAle?")
                    for i in range(2):
                        osc.timeout = 100000
                        osc.write("MEASUrement:IMMed:SOUrce1 CH1")
                        voltaje1 = osc.query('MEASUrement:IMMed:VALue?')
                        osc.write("MEASUrement:IMMed:SOUrce1 CH2")
                        voltaje2 = osc.query('MEASUrement:IMMed:VALue?')
                        # Agregar el número actual a la lista
                        temp = float(voltaje1) - float(voltaje2)
                        voltajes.append(temp)
                        
                        
                    
                    sol = sum(voltajes) / len(voltajes)
                    print("Voltajes del Canal 1:", sol)

            else:
                print("No se encontraron dispositivos Visa conectados.")
finally:
    recurso.close()
    rm.close()
    
    



    
