% Parámetros del modelo
int: n; 
int: m; 
array[1..n, 1..m] of int: demand; 
array[1..3] of int: costs; 
array[1..3] of int: capacities; 
array[1..m] of int: Ps; 
float: min_demand_percentage;
float: hydro_max_percentage;
int: hydro_max_consecutive_days;

% Variables del modelo
array[1..n, 1..3] of var 0..max(capacities): production; 
array[1..n, 1..m] of var 0..sum(capacities): client_supply; 

% Restricciones
constraint forall(d in 1..n, p in 1..3) (production[d, p] <= capacities[p]);
constraint forall(d in 1..n, s in 1..m) (client_supply[d, s] >= min_demand_percentage * demand[d, s]);
constraint forall(d in 1..n, s in 1..m) (client_supply[d, s] <= demand[d, s]);
constraint forall(d in 1..n) (sum(p in 1..3) (production[d, p]) = sum(s in 1..m) (client_supply[d, s]));

% Restricción adicional para la hidroeléctrica
constraint forall(d in 2..n) (
    (production[d-1, 2] >= hydro_max_percentage * capacities[2] /\ production[d, 2] >= hydro_max_percentage * capacities[2]) 
    -> (d - (d-1) > hydro_max_consecutive_days)
);

% Función objetivo: Maximizar la ganancia neta
var int: net_profit = sum(d in 1..n, s in 1..m) (Ps[s] * client_supply[d, s]) - sum(d in 1..n, p in 1..3) (costs[p] * production[d, p]);
solve maximize net_profit;

% Salida
% output ["Ganancia neta: \(net_profit)\n"];

% Salida
output [
    "Ganancia neta: ", show(net_profit), "\n",
    "\nProducción por planta:\n",
    "Nuclear (Día - Producción):\n"
] ++
[show(d) ++ " - " ++ show(production[d,1]) ++ "\n" | d in 1..n] ++
[
    "Hidroeléctrica (Día - Producción):\n"
] ++
[show(d) ++ " - " ++ show(production[d,2]) ++ "\n" | d in 1..n] ++
[
    "Térmica (Día - Producción):\n"
] ++
[show(d) ++ " - " ++ show(production[d,3]) ++ "\n" | d in 1..n] ++
[
    "\nSuministro a clientes:\n"
] ++
concat([
    ["Cliente ", show(s), " (Día - Suministro):\n"] ++
    [show(d) ++ " - " ++ show(client_supply[d,s]) ++ "\n" | d in 1..n]
    | s in 1..m
]);


