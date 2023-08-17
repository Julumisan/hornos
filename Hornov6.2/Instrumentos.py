# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 17:01:20 2023

@author: julu
"""

from enum import Enum

class Instrumentos(Enum):
    """Enum para representar diferentes tipos de instrumentos."""

    DAQ = 1             # Data Acquisition
    OSCILOSCOPIO = 2    # Osciloscopio
    MULTIMETRO = 3      # Multímetro
    SIMULATION = 4      # Simulación