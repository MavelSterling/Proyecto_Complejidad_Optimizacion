import tkinter as tk
from tkinter import ttk
import os

class EnergyApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Interfaz de Energía")
        self.geometry("500x400")

        ttk.Label(self, text="Número de días (n):").grid(column=0, row=0)
        self.days_var = tk.IntVar()
        ttk.Entry(self, textvariable=self.days_var).grid(column=1, row=0)

        ttk.Label(self, text="Número de clientes (m):").grid(column=0, row=1)
        self.clients_var = tk.IntVar()
        ttk.Entry(self, textvariable=self.clients_var).grid(column=1, row=1)

        ttk.Label(self, text="Costos (N, H, T):").grid(column=0, row=2)
        self.costs_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.costs_var).grid(column=1, row=2)

        ttk.Label(self, text="Capacidades (N, H, T):").grid(column=0, row=3)
        self.capacities_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.capacities_var).grid(column=1, row=3)

        # ... puedes agregar más campos según lo necesario

        ttk.Button(self, text="Ejecutar", command=self.execute_model).grid(column=1, row=10)

    def execute_model(self):
        # Captura los valores desde la interfaz y escribe el archivo Datos.dzn
        with open("Datos.dzn", "w") as file:
            file.write(f"n = {self.days_var.get()};\n")
            file.write(f"m = {self.clients_var.get()};\n")
            costs = self.costs_var.get().split(',')
            file.write(f"costs = [{costs[0]}, {costs[1]}, {costs[2]}];\n")
            capacities = self.capacities_var.get().split(',')
            file.write(f"capacities = [{capacities[0]}, {capacities[1]}, {capacities[2]}];\n")
            # ... más datos según sean necesarios

        # Ejecuta el modelo de MiniZinc
        os.system("minizinc PlantaEnergia.mzn Datos.dzn")
        # Aquí puedes añadir código para capturar la salida de MiniZinc y mostrarla en la interfaz

if __name__ == "__main__":
    app = EnergyApp()
    app.mainloop()
