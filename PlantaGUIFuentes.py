import tkinter as tk
from tkinter import ttk
import os

class EnergyApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Interfaz de Energía")
        self.geometry("600x450")

        # Campos para los datos de entrada
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

        ttk.Label(self, text="Pagos individuales por MW (m clientes):").grid(column=0, row=4)
        self.ps_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.ps_var).grid(column=1, row=4)

        ttk.Label(self, text="Porcentaje mínimo de demanda a cubrir:").grid(column=0, row=5)
        self.min_demand_percentage_var = tk.DoubleVar(value=0.50)
        ttk.Entry(self, textvariable=self.min_demand_percentage_var).grid(column=1, row=5)

        ttk.Label(self, text="Porcentaje máximo para hidroeléctrica:").grid(column=0, row=6)
        self.hydro_max_percentage_var = tk.DoubleVar(value=0.80)
        ttk.Entry(self, textvariable=self.hydro_max_percentage_var).grid(column=1, row=6)

        ttk.Label(self, text="Días máximos consecutivos a ese porcentaje:").grid(column=0, row=7)
        self.hydro_max_consecutive_days_var = tk.IntVar(value=1)
        ttk.Entry(self, textvariable=self.hydro_max_consecutive_days_var).grid(column=1, row=7)

        self.result_var = tk.StringVar(value="Ganancia neta:")
        ttk.Label(self, textvariable=self.result_var).grid(column=1, row=8)

        ttk.Button(self, text="Ejecutar", command=self.execute_model).grid(column=1, row=9)

    def execute_model(self):
        # Genera Datos.dzn con los valores de la interfaz
        with open("Datos.dzn", "w") as file:
            file.write(f"n = {self.days_var.get()};\n")
            file.write(f"m = {self.clients_var.get()};\n")
            costs = self.costs_var.get().split(',')
            file.write(f"costs = [{costs[0]}, {costs[1]}, {costs[2]}];\n")
            capacities = self.capacities_var.get().split(',')
            file.write(f"capacities = [{capacities[0]}, {capacities[1]}, {capacities[2]}];\n")
            ps = ', '.join(self.ps_var.get().split(','))
            file.write(f"Ps = [{ps}];\n")
            file.write(f"min_demand_percentage = {self.min_demand_percentage_var.get()};\n")
            file.write(f"hydro_max_percentage = {self.hydro_max_percentage_var.get()};\n")
            file.write(f"hydro_max_consecutive_days = {self.hydro_max_consecutive_days_var.get()};\n")

        # Ejecuta el modelo con el solver especificado
        result = os.popen("minizinc --solver COIN-BC PlantaEnergia.mzn Datos.dzn").read()
        self.result_var.set(result)

if __name__ == "__main__":
    app = EnergyApp()
    app.mainloop()
