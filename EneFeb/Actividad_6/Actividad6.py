import itertools
import collections
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Definir el espacio muestral
caras_dado = range(1, 21)
espacio_muestral = list(itertools.product(caras_dado, repeat=3))

# Calcular la variable aleatoria X como la suma de los valores de los tres dados
valores_X = [sum(lanzamiento) for lanzamiento in espacio_muestral]

# Contar las frecuencias de cada valor de X
frecuencias = collections.Counter(valores_X)

# Convertir los datos en un DataFrame para mejor visualización
df = pd.DataFrame(sorted(frecuencias.items()), columns=["Valor de X", "Frecuencia"])

# Crear interfaz con Tkinter
root = tk.Tk()
root.title("Espacio Muestral y Distribución de X")

# Crear un frame principal
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Crear un frame para la gráfica
graph_frame = tk.Frame(main_frame)
graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear figura para la gráfica
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(df["Valor de X"], df["Frecuencia"], color='blue', alpha=0.7)
ax.set_xlabel("Suma de los tres dados (X)")
ax.set_ylabel("Frecuencia : Probabilidad")
ax.set_title("Distribución de la suma de tres dados de 20 caras")
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Integrar la gráfica en Tkinter
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()
canvas.draw()

# Crear un frame para la tabla
table_frame = tk.Frame(main_frame)
table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Agregar título a la tabla
title_label = tk.Label(table_frame, text="Espacio Muestral", font=("Arial", 12, "bold"))
title_label.pack()

scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(table_frame, yscrollcommand=scrollbar.set, width=20, height=20, font=("Rockwell", 12))
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Llenar la tabla con los datos del espacio muestral
for i, lanzamiento in enumerate(espacio_muestral, 1):
    listbox.insert(tk.END, f"{i}: {lanzamiento}")


def cerrar():
    root.quit()

root.protocol("WM_DELETE_WINDOW", cerrar)
# Iniciar la interfaz
tk.mainloop()
