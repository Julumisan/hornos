# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 17:05:09 2023


This script interacts with VISA devices to retrieve
its information and perform additional actions on the multimeter.

@author: julu
"""

import pyvisa as visa


def visa_resource(self):
    """
    Retrieves information about VISA devices connected to the system.

    Returns:
        mult (object): Multimeter object if a device with "PRO" in its description is found, None otherwise.
    """
    self.rm = visa.ResourceManager()
    dispositivos = self.rm.list_resources()
    for device in dispositivos:         
        try:  
            resource = self.rm.open_resource(device)
            description = resource.query("*IDN?")
            print("Dispositivo Visa encontrado:")
            print(f"  Descripción: {description.strip()}")
            print(f"  Dirección: {device}")
            print("")   
            if "PRO" in description:
                multimetro = resource
                return multimetro
        except visa.VisaIOError:
            pass

def get_mult_voltage(self, mult):
    """
    Retrieves the voltage from the multimeter.

    Args:
        mult (object): Multimeter object.

    Returns:
        float: Voltage reading from the multimeter.
    """
    voltaje = mult.query("MEASure:VOLTage:DC?")
    tempG = float(voltaje) * 100
    print (tempG)
    return tempG


