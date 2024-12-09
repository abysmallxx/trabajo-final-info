import tkinter as tk
from tkinter import filedialog, messagebox
from controladores.procesamiento import Procesamiento
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import csv
from datetime import datetime

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo de Microsueños")

        self.procesador = Procesamiento()

        # Botón para generar la señal
        self.boton_generar = tk.Button(self.root, text="Generar Señal", command=self.generar_senal)
        self.boton_generar.pack(pady=20)

        # Botón para cargar el archivo CSV
        self.boton_cargar_csv = tk.Button(self.root, text="Cargar archivo CSV", command=self.cargar_csv)
        self.boton_cargar_csv.pack(pady=20)

        # Botón para ver el reporte
        self.boton_ver_reporte = tk.Button(self.root, text="Ver Reporte", command=self.ver_reporte)
        self.boton_ver_reporte.pack(pady=20)

        # Etiqueta para mostrar el estado
        self.estado_label = tk.Label(self.root, text="Estado del Conductor: Esperando señal...", font=("Arial", 14))
        self.estado_label.pack(pady=10)

        # Área para el gráfico de la señal
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(pady=20)

        # Lista para almacenar las señales generadas
        self.senales_generadas = []

    def generar_senal(self):
        tiempo, senal, estado = self.procesador.generar_senal_sintetica()
        self.estado_label.config(text=f"Estado del Conductor: {estado}")
        messagebox.showinfo("Resultado", estado)
        self.mostrar_grafico(tiempo, senal)

        # Guardar la señal generada en la lista
        self.guardar_senal(tiempo, senal, estado)

    def cargar_csv(self):
        archivo = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if archivo:
            tiempo, senal, estado = self.procesador.cargar_datos_csv(archivo)
            if tiempo is not None:
                self.estado_label.config(text=f"Estado del Conductor: {estado}")
                self.mostrar_grafico(tiempo, senal)
                self.guardar_senal(tiempo, senal, estado)
                messagebox.showinfo("Estado del Conductor", estado)
            else:
                self.estado_label.config(text="Error al cargar archivo CSV")
                messagebox.showerror("Error", estado)

    def guardar_senal(self, tiempo, senal, estado):
        # Guardar la señal en un archivo CSV o lista
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.senales_generadas.append({
            'Fecha y Hora': fecha_hora,
            'Estado': estado,
            'Tiempo': tiempo,
            'Señal': senal
        })
        # Guardar la información en un archivo CSV
        with open('reportes.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fecha_hora, estado] + list(senal))

    def ver_reporte(self):
        # Mostrar el reporte de señales generadas en una ventana
        if not self.senales_generadas:
            messagebox.showinfo("Reporte", "No hay señales generadas aún.")
            return

        reporte = "Fecha y Hora | Estado | Señal\n"
        for senal in self.senales_generadas:
            reporte += f"{senal['Fecha y Hora']} | {senal['Estado']} | {senal['Señal'][:5]}...\n"

        messagebox.showinfo("Reporte de Señales Generadas", reporte)

    def mostrar_grafico(self, tiempo, senal):
        # Limpiar el frame de los gráficos anteriores
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(tiempo, senal)
        ax.set_title("Gráfico de la Señal")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.grid(True)

        # Incrustar el gráfico en el Canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)  # Conectar el gráfico con el canvas
        canvas.draw()
        canvas.get_tk_widget().pack()  # Mostrar el gráfico en la ventana
