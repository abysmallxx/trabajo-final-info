import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Procesamiento:
    def __init__(self):
        pass

    def generar_senal_sintetica(self):
        tiempo = np.linspace(0, 10, 1000)
        ruido_normal = np.sin(tiempo) + 0.5 * np.random.randn(1000)
        ruido_microsueño = np.sin(tiempo) + 2 * np.random.randn(1000)

        if np.random.rand() > 0.5:
            senal = ruido_microsueño
            estado = "¡Alerta de sueño detectado!\n Recomendaciones: \n1. Detén el vehículo lo antes posible en un lugar seguro. \n2. Toma un descanso de al menos 20-30 minutos. \n3. Si es posible, duerme una siesta breve para recuperar energía. \n4. Evita continuar manejando si sientes fatiga."
        else:
            senal = ruido_normal
            estado = "Conductor en estado normal. Continue su camino."

        return tiempo, senal, estado

    def cargar_datos_csv(self, archivo_csv):
        try:
            # Leer los datos del archivo CSV
            df = pd.read_csv(archivo_csv)

            # Verificar que tenga las columnas necesarias
            if 'Tiempo' in df.columns and 'Señal' in df.columns:
                tiempo = df['Tiempo'].values
                senal = df['Señal'].values

                # Analizar la señal para determinar el estado
                amplitud_promedio = np.mean(np.abs(senal))
                if amplitud_promedio > 50:  # Umbral ajustable según tus datos
                    estado = "¡Alerta de sueño detectado!\n Recomendaciones: \n1. Detén el vehículo lo antes posible en un lugar seguro. \n2. Toma un descanso de al menos 20-30 minutos. \n3. Si es posible, duerme una siesta breve para recuperar energía. \n4. Evita continuar manejando si sientes fatiga."
                else:
                    estado = "Conductor en estado normal. Continue su camino."

                return tiempo, senal, estado
            else:
                return None, None, "El archivo CSV no tiene las columnas necesarias"

        except Exception as e:
            return None, None, f"Error al cargar el archivo: {e}"
    
    def graficar_senal(self, tiempo, senal):
        plt.figure(figsize=(10, 5))
        plt.plot(tiempo, senal)
        plt.title("Gráfico de la Señal")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.grid(True)
        plt.show()
