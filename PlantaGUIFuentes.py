import tkinter as tk
from tkinter import ttk
import os

class EnergyApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Interfaz de Energía")
        self.geometry("600x400")

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

        ttk.Label(self, text="Demanda (Formato: día1cliente1,día1cliente2,...,díaNclienteM):").grid(column=0, row=4, sticky='w')
        self.demand_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.demand_var, width=50).grid(column=1, row=4)

        ttk.Label(self, text="Pagos individuales por MW (cliente1,cliente2,...):").grid(column=0, row=5, sticky='w')
        self.ps_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.ps_var).grid(column=1, row=5)

        ttk.Button(self, text="Ejecutar", command=self.execute_model).grid(column=1, row=6)

        self.result_label = ttk.Label(self, text="Resultado: ")
        self.result_label.grid(column=0, row=7, columnspan=2)

    def execute_model(self):
        # Captura los valores desde la interfaz y escribe el archivo Datos.dzn
        with open("Datos.dzn", "w") as file:
            n_val = self.days_var.get()
            m_val = self.clients_var.get()
            costs = self.costs_var.get().split(',')
            capacities = self.capacities_var.get().split(',')
            demand = self.demand_var.get().split(',')
            ps = self.ps_var.get().split(',')

            # Escribiendo los valores al archivo Datos.dzn
            file.write(f"n = {n_val};\n")
            file.write(f"m = {m_val};\n")
            file.write(f"costs = [{costs[0]}, {costs[1]}, {costs[2]}];\n")
            file.write(f"capacities = [{capacities[0]}, {capacities[1]}, {capacities[2]}];\n")
            file.write(f"demand = [|{' | '.join(demand)}|];\n")  # Reestructura la demanda a un formato 2D
            file.write(f"Ps = [{', '.join(ps)}];\n")

        # Ejecuta el modelo de MiniZinc y captura el resultado
        result = os.popen("minizinc PlantaEnergia.mzn Datos.dzn").read()
        self.result_label.config(text=f"Resultado: {result}")

if __name__ == "__main__":
    app = EnergyApp()
    app.mainloop()
