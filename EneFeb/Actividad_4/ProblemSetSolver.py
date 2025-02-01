from scipy.optimize import linprog, minimize
import numpy as np
import math
from random import randint
from gurobipy import Model, GRB
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value, LpStatus

class ProblemSetSolver:
    
    def Solve_1():
        print("Ejecutando Problema 1...")
        n = 5
        c = np.array([400, 320, 300, 300])

        A = np.array([
            [-1, -1, -1, 0],  # >= n
            [-1, -1, 0, -1],  # >= n
            [0, 0, -1, 1],    # x3 = x4
            [0, 0, 1, -1]
        ])

        b = np.array([-n, -n, 0, 0])

        bounds = [(0, None), (0, None), (0, None), (0, None)]

        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

        if res.success:
            print("Resultados del Problema 1:")
            print("Valores de las variables:", res.x)
            print("Valor de la funcion objetivo:", res.fun)
        else:
            print("Error en la optimizacion del Problema 1:", res.message)
        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 1")

    def Solve_2():
        print("Ejecutando Problema 2...")
        L = math.floor(randint(10, 60))
        
        def objective(vars):
            w, h = vars
            return -(w * h)

        def constraint_1(vars):
            w, h = vars
            return w + h - L / 2

        constraints = [{'type': 'eq', 'fun': constraint_1}]
        bounds = [(0, None), (0, None)]  # w, h deben ser mayores que 0
        initial_guess = [1, 1]

        result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints, method='SLSQP')

        if result.success:
            print("Resultados del Problema 2:")
            print("Valores de las variables (w, h):", result.x)
            print("Valor maximo del area:", -result.fun)
        else:
            print("Error en la optimizacion del Problema 2:", result.message)
        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 2")

    def Solve_3():
        print("Ejecutando Problema 3...")
        print("SE UTILIZA EL MODELO ANTERIOR, NO ES NECESARIO PROGRAMAR EN ESTE PROBLEMA")
        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 3")

    def Solve_4():
        print("Ejecutando Problema 4...")
        A = 1
        J = 2
        Jo = 5
        K = 10
        n = 4  # numero de personas

        t_AJ = max(A, J)
        t_AJo = max(A, Jo)
        t_AK = max(A, K)
        t_JJo = max(J, Jo)
        t_JK = max(J, K)
        t_JoK = max(Jo, K)

        c = np.array([t_AJ, t_AJo, t_AK, t_JJo, t_JK, t_JoK, A, J, Jo, K])

        A_ = np.array([
            [-1, -1, -1, 0, 0, 0, 1, 0, 0, 0], # >= 1
            [-1, 0, 0, -1, -1, 0, 0, 1, 0, 0], # >= 1
            [0, -1, 0, -1, 0, -1, 0, 0, 1, 0], # >= 1
            [0, 0, -1, 0, -1, -1, 0, 0, 0, 1], # >= 1
            [-1, -1, -1, -1, -1, -1, 0, 0, 0, 0], # >= n-1 ... >= 3
            [0, 0, 0, 0, 0, 0, -1, -1, -1, -1]  # >= n-2 ... >= 2
        ])

        b = np.array([-1, -1, -1, -1, -(n-1), -(n-2)])

        bounds = [(0, None)] * len(c)

        res = linprog(c, A_ub=A_, b_ub=b, bounds=bounds, method='highs')

        if res.success:
            print("Resultados del Problema 4:")
            print("Valores de las variables:", res.x)
            print("Valor de la funcion objetivo:", res.fun)
        else:
            print("Error en la optimizacion del Problema 4:", res.message)
        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 4")

    def Solve_5():
        print("Ejecutando Problema 5...")
        
        def objective(vars):
            x1, x2, y1, y2 = vars
            return -(0.3 * x1 * y1 + 0.5 * x2 * y2 + 0.2 * x2 * y1 + 0.1 * x1 * y2)

        def constraint_1(vars):
            x1, x2, y1, y2 = vars
            return x1 + x2 - 1  # x1 + x2 = 1

        def constraint_2(vars):
            x1, x2, y1, y2 = vars
            return y1 + y2 - 1  # y1 + y2 = 1

        constraints = [
            {'type': 'eq', 'fun': constraint_1},
            {'type': 'eq', 'fun': constraint_2}
        ]

        bounds = [(0, 1), (0, 1), (0, 1), (0, 1)]  # x1, x2, y1, y2 deben estar entre 0 y 1

        initial_guess = [0.3, 0.7, 0.4, 0.6]

        result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints, method='SLSQP')

        if result.success:
            print("Resultados del Problema 5:")
            print("Valores de las variables (x1, x2, y1, y2):", result.x)
            print("Valor maximo de bateo:", -result.fun)
        else:
            print("Error en la optimizacion del Problema 5:", result.message)
        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 5")

    def Solve_6():
        print("Ejecutando Problema 6...")
        
        prob = LpProblem("Minimizar_Tiempo", LpMinimize)

        x = {(r, i): LpVariable(f"x_{r}_{i}", cat="Binary") for r in range(1, 9) for i in range(1, 4)}
        c = {(r, i): LpVariable(f"c_{r}_{i}", lowBound=0, upBound=6, cat="Integer") for r in range(0, 9) for i in range(1, 4)}

        for i in range(1, 4):
            prob += c[(0, i)] == 0

        for r in range(1, 9):
            for i in range(1, 4):
                prob += c[(r, i)] == c[(r - 1, i)] + x[(r, i)]

        z1 = {r: LpVariable(f"z1_{r}", cat="Binary") for r in range(1, 9)}
        z2 = {r: LpVariable(f"z2_{r}", cat="Binary") for r in range(1, 9)}
        z3 = {r: LpVariable(f"z3_{r}", cat="Binary") for r in range(1, 9)}

        for r in range(1, 9):
            prob += c[(r - 1, 1)] <= 5 + 6 * (1 - z1[r])
            prob += x[(r, 1)] <= z1[r]
    
            prob += c[(r - 1, 1)] - c[(r - 1, 2)] >= 1 - 6 * (1 - z2[r])
            prob += x[(r, 2)] <= z2[r]
    
            prob += c[(r - 1, 2)] - c[(r - 1, 3)] >= 1 - 6 * (1 - z3[r])
            prob += x[(r, 3)] <= z3[r]

        prob += c[(8, 1)] + c[(8, 2)] + c[(8, 3)] == 18

        max_time = {r: LpVariable(f"max_time_{r}", lowBound=0) for r in range(1, 9)}
        for r in range(1, 9):
            prob += max_time[r] >= 20 * x[(r, 1)]
            prob += max_time[r] >= 25 * x[(r, 2)]
            prob += max_time[r] >= 20 * x[(r, 3)]

        prob += lpSum(max_time[r] for r in range(1, 9))

        prob.solve()

        for r in range(1, 9):
            print(f"Ronda {r}:", {f"x1": x[(r, 1)].varValue, f"x2": x[(r, 2)].varValue, f"x3": x[(r, 3)].varValue})

        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 6")

    def Solve_7():
        print("Ejecutando Problema 7...")
        capas = [1, 2, 3, 4]

        x = LpVariable.dicts('x', (capas, capas), cat='Integer', lowBound=0)

        prob = LpProblem("Invertir_piramide", LpMinimize)

        prob += lpSum(x[punto][capa] for punto in capas for capa in capas if punto != capa), "Minimizar_movimientos"

        prob += lpSum(x[punto][4] for punto in capas if punto != 4) == 3, "Restriccion_capa_4"
        prob += lpSum(x[punto][3] for punto in capas if punto != 3) == 1, "Restriccion_capa_3"
        prob += lpSum(x[punto][2] for punto in capas if punto != 2) == 0, "Restriccion_capa_2"
        prob += lpSum(x[punto][1] for punto in capas if punto != 1) == 0, "Restriccion_capa_1"

        prob += lpSum(x[1][capa] for capa in capas if capa != 1) == 3, "Restriccion_origen_capa_1"
        prob += lpSum(x[2][capa] for capa in capas if capa != 2) == 1, "Restriccion_origen_capa_2"
        prob += lpSum(x[3][capa] for capa in capas if capa != 3) == 0, "Restriccion_origen_capa_3"
        prob += lpSum(x[4][capa] for capa in capas if capa != 4) == 0, "Restriccion_origen_capa_4"


        prob.solve()

        if LpStatus[prob.status] == 'Optimal':
            total_movimientos = value(prob.objective)
            print(f"Total de movimientos realizados: {total_movimientos}")

            for punto in capas:
                for capa in capas:
                    k = value(x[punto][capa])
                    if punto != capa and k >= 1:
                        print(f"Se movieron {int(k)} puntos de la capa {punto} a la capa {capa}")
        else:
            print("No se encontro solucion optima.")

        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 7")

    def Solve_8():
        print("Ejecutando Problema 8...")
        C = 2
        S = 3

        c = np.array([C, S])
        
        A_eq = np.array([
            [1, -1] # x = y
        ])

        b_eq = np.array([0])

        A_ub = np.array([
            [1, 0], # <= 12     maxima cantidad de cortes
            [0, -1] # >= 4 minima cantidad de soldaduras
        ])

        b_ub = np.array([12, -4])

        bounds = [(0, None)] * len(c)

        res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if res.success:
            print("Resultados del Problema 8:")
            print("Valores de las variables:", res.x)
            print("Valor de la funcion objetivo:", res.fun)
        else:
            print("Error en la optimizacion del Problema 8:", res.message)
        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 8")

    def Solve_9():
        print("Ejecutando Problema 9...")

        # Definir el conjunto de cuadros numerados del 1 al 99
        N = list(range(1, 100))  # 1 a 99
        M = [9 * i for i in range(1, 12)]  # Múltiplos de 9 hasta 99

        # Definir el problema de minimización
        model = LpProblem(name="minimize-rewards", sense=LpMinimize)

        # Definir variables de decisión (Recompensas R_N para cada cuadro)
        R = {n: LpVariable(name=f"R_{n}", lowBound=0, upBound=20) for n in N}

        # Función objetivo: minimizar la suma total de las recompensas
        model += lpSum(R[n] for n in N), "Total_Rewards"

        # Restricciones
        for n in M:
            model += R[n] == 0, f"Zero_Reward_{n}"  # Múltiplos de 9 tienen recompensa 0

        for n in N:
            if n not in M:
                model += R[n] >= 1, f"Min_Reward_{n}"  # Los demás cuadros tienen recompensa >= 1

        # Resolver el problema
        model.solve()

        # Imprimir resultados
        for n in N:
            #print(f"R_{n} = {R[n].varValue}", end=" ")
            print(f"{R[n].varValue}", end="|")
            if n % 9 == 0: print("\n----------------------------------------------")

        # Mostrar el valor óptimo de la función objetivo
        print(f"Costo total minimo: {model.objective.value()} dolares")

        print("SE HA COMPLETADO LA EJECUCION DEL PROBLEMA 9")
