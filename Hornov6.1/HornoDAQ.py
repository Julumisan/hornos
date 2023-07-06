# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:35:25 2023

@author: Julu
"""


from art_daq import daq
import random

class HornoDAQ:
    def __init__(self, device_name, horno_control):
        self.device_name = device_name
        self.chan_d = self.device_name + "/port0/line1"
        self.chan_a = self.device_name + "/ao0"
        self.horno_control = horno_control

    def warm_state(self):
        """Este método establece la salida analógica en 0V
        y la salida digital en HIGH (5V) 
        """
        print(daq.set_voltage_analogic(self.chan_a, 0))
        daq.set_voltage_digital(self.chan_d, True)

    def cold_state(self):
        """Este método establece la salida analógica en 5V
        y la salida digital en LOW (0V) 
        """
        daq.set_voltage_digital(self.chan_d, False)
        print(daq.set_voltage_analogic(self.chan_a, 5))

    def mild_state(self):
        """Este método establece la salida analógica en 2.5V
        y la salida digital en LOW (0V) 
        """
        daq.set_voltage_digital(self.chan_d, False)
        print(daq.set_voltage_analogic(self.chan_a, 2.5))

    def transform_voltage_temp(self):
        """
        Convierte la lectura de voltaje del canal analógico AI0 en una lectura de temperatura en grados Celsius.
        Multiplica la lectura de voltaje por 100 y devuelve el valor de temperatura resultante.
    
        Returns:
            El valor de la temperatura en grados Celsius.
        """
        # Cambiar de Voltaje a temperatura
        temp = daq.get_voltage_analogic(self.device_name + "/ai0") * 100
        # print("Temperatura leída: {:.2f} ºC".format(temp))
        return temp
    
    
    def random_number_between_20_and_40(self, last_number=None, increment=0):
        """
        Genera un número pseudoaleatorio entre 20 y 40, con una variación máxima de 0.2 respecto al número anterior.
        Permite un incremento por parámetro para simular la temperatura en ausencia de la DAQ.
    
        Args:
            last_number: El último número generado (opcional).
            increment: El valor de incremento a sumar al número generado (opcional).
    
        Returns:
            El número aleatorio generado, con un máximo de variación de 0.2 respecto al número anterior.
        """
    
        # Definir el rango de números permitidos
        min_number = 20
        max_number = 40
        # Establecer la diferencia máxima permitida entre el último número generado y el siguiente
        allowed_diff = 0.2
    
        # Si no se ha generado un número previamente (last_number es None),
        # generar un número aleatorio entre el rango permitido
        if last_number is None:
            return random.uniform(min_number, max_number)
    
        # Establecer el límite inferior para el próximo número aleatorio,
        # asegurándose de que no sea menor que el mínimo permitido
        min_limit = max(min_number, last_number - allowed_diff)
    
        # Establecer el límite superior para el próximo número aleatorio,
        # asegurándose de que no sea mayor que el máximo permitido
        max_limit = min(max_number, last_number + allowed_diff)
    
        # Generar y devolver un número aleatorio entre los límites calculados,
        # sumando el valor del incremento dado por parámetro
        return random.uniform(min_limit, max_limit) + increment