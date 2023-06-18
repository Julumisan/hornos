# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 17:04:51 2023

This script interacts with VISA devices to retrieve
its information and perform additional actions on the oscilloscope.

@author: julu
"""

import pyvisa as visa
import time


def visa_resource(self):
    """
    Retrieves information about VISA devices connected to the system.

    Returns:
        osc (object): Oscilloscope object if a device with "MSO" in its description is found, None otherwise.
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
            # Additional actions if the description contains "MSO"
            if "MSO" in description:
                recurso.write("*RST")
                print("Additional action performed")
                recurso.write("HORIZONTAL:MAIN:SCALE 1E-3")
                recurso.write("CH1:SCALE 100E-03")
                recurso.write("CH2:SCALE 100E-03")
                recurso.write("CH1:POSition -3")
                recurso.write("CH2:POSition -3")
                recurso.write("MEASUrement:MEAS1:STATE ON")
                recurso.write("MEASUrement:MEAS1:SOURCE1 CH1")
                recurso.write("MEASUrement:MEAS1:TYPe MEAN")
                recurso.write("MEASUrement:MEAS2:STATE ON")
                recurso.write("MEASUrement:MEAS2:SOURCE1 CH2")
                recurso.write("MEASUrement:MEAS2:TYPe MEAN")
                recurso.write("MEASUrement:MEAS3:STATE ON")
                recurso.write("MEASUrement:MEAS3:SOURCE1 MATH1")
                recurso.write("MEASUrement:MEAS3:TYPe MEAN")
                recurso.write("SELECT:CH1 ON;CH2 ON")
                recurso.write("MATH1:DEFINE \"CH1-CH2\"")
                recurso.write("SELECT:MATH1 ON")
                recurso.write("MATH1:VERTICAL:POSition -3")
                recurso.write("MATH1:SCALE 100E-03")
                time.sleep(1)
                recurso.write(":ACQUIRE:STATE ON")
                osc = recurso
                # Get voltages from Channel 1
                return osc
            else:
                print("No Visa devices found.")
    except:
        recurso.close()
        self.rm.close()


def get_osc_voltage(self, osc):
    """
    Retrieves the voltages from the oscilloscope.

    Args:
        osc (object): Oscilloscope object.

    Returns:
        float: Average of the voltages CH1 minus CH2
        
    """
    voltajes = []
    print(osc.write("MEASUrement:IMMed:TYPe MEAN"))
    scale = osc.write("CH1:SCAle?") #Pa porsi
    for i in range(2):
        osc.timeout = 100000
        osc.write("MEASUrement:IMMed:SOUrce1 CH1")
        voltaje1 = osc.query('MEASUrement:IMMed:VALue?')
        osc.write("MEASUrement:IMMed:SOUrce1 CH2")
        voltaje2 = osc.query('MEASUrement:IMMed:VALue?')
        # Add the current number to the list
        temp = float(voltaje1) - float(voltaje2)
        voltajes.append(temp)
    tempG = (sum(voltajes) / len(voltajes)) * 100
    print("Voltages from Channel 1:", tempG)
    return tempG
        
        
