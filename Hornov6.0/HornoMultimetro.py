# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 17:05:09 2023

@author: julu
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 17:05:09 2023


This script interacts with VISA devices to retrieve
its information and perform additional actions on the multimeter.

Author: julu
"""

import pyvisa as visa
import time

def visa_resource(self):
    """
    Retrieves information about VISA devices connected to the system.

    Returns:
        mult (object): Multimeter object if a device with "PRO" in its description is found, None otherwise.
    """
    try:
        self.rm = visa.ResourceManager()
        dispositivos = self.rm.list_resources()

        for device in dispositivos:
            recurso = self.rm.open_resource(device)
            description = recurso.query("*IDN?")
            print("Visa Device Found:")
            print(f"  Description: {description.strip()}")
            print(f"  Address: {device}")
            print("")
            # Additional actions if the description contains "PRO"
            if "PRO" in description:
                recurso.write("SENS:FUNC1 \"VOLT:DC\" ")
                mult = recurso
            else:
                print("No Visa devices found.")
            return mult
    except:
        recurso.close()
        self.rm.close()

def get_mult_voltage(self, mult):
    """
    Retrieves the voltage from the multimeter.

    Args:
        mult (object): Multimeter object.

    Returns:
        float: Voltage reading from the multimeter.
    """
    voltaje = mult.query(":DATA?")
    tempG = voltaje * 100
    return tempG