# coding=utf-8
import tkinter as tk
from tkinter import ttk, scrolledtext
import os

class EnergyApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Interfaz de Energía")
        self.state("zoomed")
        
        # Frame para los datos de entrada (lado izquierdo)
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Frame para los resultados (lado derecho)
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        
        # Campos para los datos de entrada
        ttk.Label(left_frame, text="Número de días (n):").grid(column=0, row=0)
        self.days_var = tk.IntVar()
        ttk.Entry(left_frame, textvariable=self.days_var).grid(column=1, row=0)

        ttk.Label(left_frame, text="Número de clientes (m):").grid(column=0, row=1)
        self.clients_var = tk.IntVar()
        ttk.Entry(left_frame, textvariable=self.clients_var).grid(column=1, row=1)

        ttk.Label(left_frame, text="Costos (N, H, T):").grid(column=0, row=2)
        self.costs_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.costs_var).grid(column=1, row=2)

        ttk.Label(left_frame, text="Capacidades (N, H, T):").grid(column=0, row=3)
        self.capacities_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.capacities_var).grid(column=1, row=3)

        ttk.Label(left_frame, text="Pagos individuales por MW (m clientes):").grid(column=0, row=4)
        self.ps_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.ps_var).grid(column=1, row=4)

        ttk.Label(left_frame, text="Porcentaje mínimo de demanda a cubrir:").grid(column=0, row=5)
        self.min_demand_percentage_var = tk.DoubleVar(value=0.50)
        ttk.Entry(left_frame, textvariable=self.min_demand_percentage_var).grid(column=1, row=5)

        ttk.Label(left_frame, text="Porcentaje máximo para hidroeléctrica:").grid(column=0, row=6)
        self.hydro_max_percentage_var = tk.DoubleVar(value=0.80)
        ttk.Entry(left_frame, textvariable=self.hydro_max_percentage_var).grid(column=1, row=6)

        ttk.Label(left_frame, text="Días máximos consecutivos a ese porcentaje:").grid(column=0, row=7)
        self.hydro_max_consecutive_days_var = tk.IntVar(value=1)
        ttk.Entry(left_frame, textvariable=self.hydro_max_consecutive_days_var).grid(column=1, row=7)

        ttk.Label(left_frame, text="Demanda diaria (fila por día, columna por cliente):").grid(column=0, row=8, sticky='w')
        self.demand_txt = scrolledtext.ScrolledText(left_frame, width=30, height=5)
        self.demand_txt.grid(column=1, row=8)

        self.result_var = tk.StringVar(value="Ganancia neta:")
        ttk.Label(right_frame, textvariable=self.result_var).grid(column=1, row=0)  # Mostrar resultados en el frame derecho

        ttk.Button(left_frame, text="Ejecutar", command=self.execute_model).grid(column=1, row=10)


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
            
            demand_data = self.demand_txt.get("1.0", tk.END).strip().split('\n')
            demand_rows = '|\n'.join(demand_data)
            file.write(f"demand = [|{demand_rows}|];\n")

        # Ejecuta el modelo con el solver especificado
        cmd_result = os.popen("/Applications/MiniZincIDE.app/Contents/Resources/minizinc --solver COIN-BC PlantaEnergia.mzn Datos.dzn").read()  
        print(" ") 
        print(" ")     
        print(cmd_result)
        self.result_var.set(cmd_result)

if __name__ == "__main__":
    app = EnergyApp()
    app.mainloop()
