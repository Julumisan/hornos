# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:34:57 2023

@author: Julu


v4.4
 
Botones disabled, añado el botón de inicio para adquisicion


"""

import csv
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk


class HornoGUI:
    
    def __init__(self, horno_control, horno_daq):
        """
        Inicializa la clase HornoControlUI.
        
        Args:
            horno_control (HornoControl): Instancia de la clase HornoControl.
            horno_daq (HornoDAQ): Instancia de la clase HornoDAQ.
        """
        self.horno_control = horno_control
        self.horno_daq = horno_daq
        self.__init_ui__()
    
    def __init_ui__(self):
        """
        Crea la interfaz gráfica de usuario utilizando tkinter y ttk.
        """
        # Crea la ventana principal de la aplicación.
        self.horno_control.root = tk.Tk()

        # Crea un marco para contener los widgets.
        self.horno_control.frame = ttk.Frame(self.horno_control.root)
        self.horno_control.frame.pack()

        # Crea una figura y ejes utilizando la interfaz orientada a objetos.
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        
        # Crea una gráfica utilizando matplotlib y la coloca en la parte superior del marco.
        self.horno_control.canvas = FigureCanvasTkAgg(fig, master=self.horno_control.frame)
        self.horno_control.canvas.draw()
        self.horno_control.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Crea un marco para contener los widgets de temperatura máxima y mínima.
        temp_frame = tk.Frame(self.horno_control.frame)
        temp_frame.pack(side=tk.TOP, padx=20, pady=20, anchor="center")

        # Crea una subventana para los widgets relacionados con la temperatura mínima.
        min_temp_frame = tk.Frame(temp_frame, bg='lightgray')
        min_temp_frame.pack(side=tk.LEFT)

        # Crea una subventana para los widgets relacionados con la temperatura máxima.
        max_temp_frame = tk.Frame(temp_frame, bg='lightgray')
        max_temp_frame.pack(side=tk.LEFT)
        
        # Crea una etiqueta para la temperatura máxima y la agrega a la subventana.
        self.horno_control.max_temp_label = tk.Label(max_temp_frame, text="Temperatura Máxima:", font=("Arial", 14), bg='lightgray')
        self.horno_control.max_temp_label.pack(side=tk.TOP, padx=20)

        # Crea una caja de texto para ingresar la temperatura máxima y la agrega a la subventana.
        self.horno_control.max_temp_entry = ttk.Entry(max_temp_frame)
        self.horno_control.max_temp_entry.pack(side=tk.TOP)

        # Crea un botón para actualizar la temperatura máxima y lo agrega a la subventana.
        self.horno_control.update_max_temp_button = ttk.Button(
            max_temp_frame, text="Actualizar Máxima", command=self.update_max_temp)
        self.horno_control.update_max_temp_button.pack(side=tk.TOP, pady=10)
        
        # Crea un botón para Iniciar adquisición datos.
        self.horno_control.iniciar_adquisicion_button = ttk.Button(
        self.horno_control.root, text="Iniciar adquisición datos", command=self.iniciar_adquisicion, state='normal')
        self.horno_control.iniciar_adquisicion_button.pack(side=tk.TOP, pady=10)
        
        # Crea una etiqueta para la temperatura mínima y la agrega a la subventana.
        self.horno_control.min_temp_label = tk.Label(min_temp_frame, text="Temperatura Mínima:", font=("Arial", 14), bg='lightgray')
        self.horno_control.min_temp_label.pack(side=tk.TOP, padx=20)

        # Crea una caja de texto para ingresar la temperatura mínima y la agrega a la subventana.
        self.horno_control.min_temp_entry = ttk.Entry(min_temp_frame)
        self.horno_control.min_temp_entry.pack(side=tk.TOP)

        # Crea un botón para actualizar la temperatura mínima y lo agrega a la subventana.
        self.horno_control.update_min_temp_button = ttk.Button(
            min_temp_frame, text="Actualizar Mínima", command=self.update_min_temp)
        self.horno_control.update_min_temp_button.pack(side=tk.TOP, pady=10)

        # Crea un botón para salir de la aplicación y lo agrega a la ventana principal.
        self.horno_control.exitButton = ttk.Button(
            self.horno_control.root, text="SALIR", command=self.horno_control.root.destroy)
        self.horno_control.exitButton.pack(side=tk.BOTTOM, pady=10)

        # Crea el botón de guardar los datos
        self.horno_control.save_button = ttk.Button(
            self.horno_control.root, text="Guardar datos", command=self.exportar_datos_csv)
        self.horno_control.save_button.pack(side=tk.BOTTOM, pady=10)
        # Crea el botón de pausa
        self.horno_control.pause_button = ttk.Button(
        self.horno_control.root, text="Pausar", command=self.horno_control.toggle_pause)
        self.horno_control.pause_button.pack(side=tk.BOTTOM, pady=10)
    
        # Crea una animación para actualizar la gráfica de temperatura en tiempo real.
        self.horno_control.ani = animation.FuncAnimation(
            fig, self.grafica_real_time, interval=500)
        self.horno_control.ani_running = self.horno_control.canvas.get_tk_widget().after(
            0, self.horno_control.ani.event_source.start)
        
        # Cambia el estado inicial de los otros botones a "disabled"
        # self.horno_control.exitButton.configure(state='disabled')
        self.horno_control.save_button.configure(state='disabled')
        self.horno_control.pause_button.configure(state='disabled')
        self.horno_control.update_max_temp_button.configure(state='disabled')
        self.horno_control.update_min_temp_button.configure(state='disabled')

    
    def grafica_real_time(self, i: int):
        """
        Actualiza la gráfica de temperatura en tiempo real.
    
        Args:
            i (int): El número de veces que se ha llamado a la función.
        """
        if self.horno_control.started and not self.horno_control.paused:
            self.horno_control.pause_button.config(text="Pausar")
            self.horno_control.count += 1
            self.update_temperature_data()
            self.update_temperature_graph()
            self.check_temperature_range()
        else:
            self.horno_control.pause_button.config(text="Reanudar")
    
    def update_temperature_data(self):
        """Actualiza los datos de temperatura."""
        self.horno_control.x.append(self.horno_control.count * 0.5)
        self.horno_control.tempG = self.horno_daq.transform_voltage_temp()
        self.horno_control.y1.append(self.horno_control.tempG)
        self.horno_control.y2.append(self.horno_control.max_temp)
        self.horno_control.y3.append(self.horno_control.min_temp)
        print(f"Tiempo: {self.horno_control.count * 0.5:.2f}s, Temperatura {self.horno_control.tempG:.2f}")
    
    def update_temperature_graph(self):
        """Actualiza la gráfica de temperatura."""
        self.ax.clear()
        self.ax.plot(self.horno_control.x, self.horno_control.y1, label='Temperatura')
        self.ax.plot(self.horno_control.x, self.horno_control.y2, label='Temp. Máx')
        self.ax.plot(self.horno_control.x, self.horno_control.y3, label='Temp. Mín')
        self.ax.legend(loc='best')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Temperatura (°C)')
    
    def check_temperature_range(self):
        """Verifica si la temperatura está dentro del rango establecido."""
        if self.horno_control.max_temp < self.horno_control.tempG:
            print("Estamos calientes")
            self.horno_daq.warm_state()
    
        elif self.horno_control.tempG < self.horno_control.min_temp:
            print("Estamos frios")
            self.horno_daq.cold_state()
        else:
            print("tamo bien")
            self.horno_daq.mild_state()
    
    def update_max_temp(self):
        """
        Actualiza la temperatura máxima con el valor ingresado por el usuario.
        """
        try:
            temp_str = self.horno_control.max_temp_entry.get()
            if temp_str:
                temp = float(temp_str)
                if self.is_valid_temperature_range(self.horno_control.min_temp, temp):
                    self.horno_control.max_temp = temp
                else:
                    tk.messagebox.showerror("Error", "La temperatura máxima no puede ser menor o igual a la temperatura mínima.")
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número válido para la temperatura máxima")
    
    def update_min_temp(self):
        """
        Actualiza la temperatura mínima con el valor ingresado por el usuario.
        """
        try:
            temp_str = self.horno_control.min_temp_entry.get()
            if temp_str:
                temp = float(temp_str)
                if self.is_valid_temperature_range(temp, self.horno_control.max_temp):
                    self.horno_control.min_temp = temp
                else:
                    tk.messagebox.showerror("Error", "La temperatura mínima no puede ser mayor o igual a la temperatura máxima.")
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número válido para la temperatura mínima")
    
    def exportar_datos_csv(self):
        """
        Exporta los datos de la medición en un archivo CSV.
        
        Primero, abre un diálogo para seleccionar la ruta y el nombre del archivo. Luego,
        escribe los datos en el archivo CSV.
        """
        # Obtener los datos a exportar
        x = self.horno_control.x
        y1 = self.horno_control.y1
        y2 = self.horno_control.y2
        y3 = self.horno_control.y3
        
        # Abrir un cuadro de diálogo para seleccionar la ruta y el nombre del archivo
        nombre_archivo = tk.filedialog.asksaveasfilename(defaultextension=".csv")
        if nombre_archivo:
            # Escribir los datos en el archivo CSV
            with open(nombre_archivo, 'w', newline='') as archivo_csv:
                writer = csv.writer(archivo_csv)
                writer.writerow(["Tiempo (s)", "Temperatura (°C)", "Temp. Máx (°C)", "Temp. Mín (°C)"])
                for i in range(len(x)):
                    writer.writerow([x[i], y1[i], y2[i], y3[i]])
            print("Datos exportados exitosamente.")
    
    def iniciar_adquisicion(self):
        """
        Inicia la adquisición de datos y actualiza el estado de los botones de la interfaz.
        """
        self.horno_control.iniciar_adquisicion_button.configure(state='disabled')
        self.horno_control.exitButton.configure(state='normal')
        self.horno_control.save_button.configure(state='normal')
        self.horno_control.pause_button.configure(state='normal')
        self.horno_control.update_max_temp_button.configure(state='normal')
        self.horno_control.update_min_temp_button.configure(state='normal')
        self.horno_control.toggle_start()
        self.horno_control.toggle_pause()
        
        
    def is_valid_temperature_range(self, new_min_temp: float, new_max_temp: float) -> bool:
        """
        Verifica si el rango de temperatura ingresado es válido.
        
        Args:
            new_min_temp (float): La nueva temperatura mínima propuesta.
            new_max_temp (float): La nueva temperatura máxima propuesta.
            
        Returns:
            bool: True si el rango es válido, False en caso contrario.
        """
        return new_min_temp < new_max_temp
        
    def start(self):
        """
        Inicia la interfaz gráfica de usuario (GUI).
        """
        self.setup_gui()
        tk.mainloop()