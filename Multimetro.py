# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:23:42 2023

@author: Juan Luis
"""
import pyvisa
import warnings

# Configurar tracemalloc en True para obtener traza de seguimiento
warnings.filterwarnings("default", category=ResourceWarning)

def obtener_info_multimetro():
    rm = pyvisa.ResourceManager()
    recursos = rm.list_resources()
    print(recursos)

    for recurso in recursos:
        try:
            with rm.open_resource(recurso, write_termination='\n') as inst:
                inst.query("SENS:FUNC1 \"VOLT:AC\" ")
        except pyvisa.Error as e:
            print(f"Error al comunicarse con el multímetro en {recurso}: {e}")
            # Me da timeout, pero realmente si realiza el cambio

# Ejecutar el script
if __name__ == '__main__':
    obtener_info_multimetro()