import random

# CONVERSIÓN DEL TABLERO 
def conversion(tablero):
    conversion_parcial = ["".join(fila) for fila in tablero]
    conversion_tablero = "\n".join(conversion_parcial)
    return conversion_tablero

# DISTANCIA MANHATAN
def distancia_manh(tablero, xr, yr, xg, yg):
    distancia= abs(xr - xg) + abs(yr - yg)
    return distancia

# MOVIMIENTOS POSIBLES
def movimientos_posibles(x, y, dimension):
    movimientos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < dimension and 0 <= ny < dimension:
            movimientos.append((nx, ny))
    return movimientos

# MINIMAX, para el raton
def minimax_raton(xr, yr, xg, yg, tablero, profundidad, max_turno, dimension):
    if profundidad == 0 or (xr == xg and yr == yg):
        distancia=distancia_manh(tablero, xr, yr, xg, yg)
        return distancia, (xr, yr)

    if max_turno:                          # TURNO RATON, que busca maximizar
        max_eval = -float("inf")
        mejor_mov = (xr, yr)
        movimientos_permitidos = movimientos_posibles(xr, yr, dimension)
        for nx, ny in movimientos_permitidos:

            distancia , _ = minimax_raton(nx, ny, xg, yg, tablero, profundidad - 1, False, dimension)

            if distancia > max_eval:
                max_eval = distancia
                mejor_mov = (nx, ny)
        return max_eval, mejor_mov
    else:                                  # TURNO DEL GATO, que busca minimizar
        min_eval = float("inf")
        peor_mov = (xg, yg)
        movimientos_permitidos=movimientos_posibles(xg, yg, dimension)
        for nx, ny in movimientos_permitidos:

            distancia, _ = minimax_raton(xr, yr, nx, ny, tablero, profundidad - 1, True, dimension)

            if distancia < min_eval:
                min_eval = distancia
                peor_mov = (nx, ny)
        return min_eval, peor_mov

# MOVIMIENTO DEL GATO
turno=0 
def movimiento_del_gato(tablero, xg, yg, turno):
    while True:
        movimiento = input("Ingrese el movimiento del gato; W:Arriba A:Izquierda S:Abajo D:Derecha: ").lower()
        turno=turno+1
        if movimiento == "w" and xg - 1 >= 0:
            tablero[xg][yg] = "⬜"
            xg -= 1
            tablero[xg][yg] = "🐱"
            break
        elif movimiento == "s" and xg + 1 < dimension:
            tablero[xg][yg] = "⬜"
            xg += 1
            tablero[xg][yg] = "🐱"
            break
        elif movimiento == "a" and yg - 1 >= 0:
            tablero[xg][yg] = "⬜"
            yg -= 1
            tablero[xg][yg] = "🐱"
            break
        elif movimiento == "d" and yg + 1 < dimension:
            tablero[xg][yg] = "⬜"
            yg += 1
            tablero[xg][yg] = "🐱"
            break
        else:
            print("Movimiento no válido. Intente de nuevo.")
    return tablero, xg, yg, turno

# INICIO DEL JUEGO
dimension = int(input("Ingrese la cantidad de filas del tablero: "))
dimension=7
tablero = [["⬜" for _ in range(dimension)] for _ in range(dimension)]

# POSICIONES INICIALES
gato = "🐱"
raton = "🐭"
xg, yg = 0, 0
xr, yr = random.randint(0, dimension - 1), random.randint(0, dimension - 1)
tablero[xg][yg] = gato
tablero[xr][yr] = raton

print("\nEstado inicial del tablero:")
print(conversion(tablero))

# BUCLE HASTA TERMINAR
while True:
    # TURNO DEL RATÓN, AUTOMATICO
    print("\nTurno del ratón 🐭 (IA):")
    _, (xr_nuevo, yr_nuevo) = minimax_raton(xr, yr, xg, yg, tablero, 3, True, dimension)
    tablero[xr][yr] = "⬜"
    xr, yr = xr_nuevo, yr_nuevo
    tablero[xr][yr] = raton
    print(conversion(tablero))

    if (xr, yr) == (xg, yg) :
        print("¡El gato atrapó al ratón! 🐱🏁")
        break
    elif turno>=12:
        print("Tequedaste sin mivmientos, el raton ha escapado")
        break

    # TURNO DEL GATO, MANUAL
    print("\nTurno del gato 🐱:")
    tablero, xg, yg, turno = movimiento_del_gato(tablero, xg, yg, turno)
    print(conversion(tablero))

    if (xr, yr) == (xg, yg):
        print("¡El gato atrapó al ratón! 🐱🏁")
        break
    elif turno>=12:
        print("Tequedaste sin mivmientos, el raton ha escapado")
        break
