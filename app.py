import heapq

BLANCO, ROJO, VERDE, AZUL, AMARILLO = "\033[47m  \033[m", "\033[41m  \033[m", "\033[42m  \033[m", "\033[44m  \033[m", "\033[43m  \033[m"
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Nodo:
    def __init__(self, posicion, g=0, h=0, padre=None):
        self.posicion = posicion
        self.g = g
        self.h = h
        self.f = g + h
        self.padre = padre

    def __lt__(self, other):
        return self.f < other.f

def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def busqueda(tablero, inicio, fin):
    lista_abierta = []
    heapq.heappush(lista_abierta, Nodo(inicio, 0, distancia_manhattan(inicio, fin)))
    lista_cerrada = set()
    nodos_abiertos = {inicio: 0}

    while lista_abierta:
        nodo_actual = heapq.heappop(lista_abierta)
        lista_cerrada.add(nodo_actual.posicion)

        if nodo_actual.posicion == fin:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1]

        for direccion in DIRECCIONES:
            posicion_vecina = (nodo_actual.posicion[0] + direccion[0], nodo_actual.posicion[1] + direccion[1])

            if (0 <= posicion_vecina[0] < len(tablero) and
                0 <= posicion_vecina[1] < len(tablero) and
                tablero[posicion_vecina[0]][posicion_vecina[1]] != ROJO and
                posicion_vecina not in lista_cerrada):

                g_nuevo = nodo_actual.g + 1
                if posicion_vecina not in nodos_abiertos or g_nuevo < nodos_abiertos[posicion_vecina]:
                    nodo_vecino = Nodo(posicion_vecina, g_nuevo, distancia_manhattan(posicion_vecina, fin), nodo_actual)
                    heapq.heappush(lista_abierta, nodo_vecino)
                    nodos_abiertos[posicion_vecina] = g_nuevo
    return None

def imprimir_mapa(tablero, inicio=None, fin=None, camino=None):
    for fila in range(len(tablero)):
        for columna in range(len(tablero[fila])):
            if (fila, columna) == inicio:
                print(VERDE, end='')
            elif (fila, columna) == fin:
                print(AZUL, end='')
            elif camino and (fila, columna) in camino:
                if (fila, columna) == inicio:
                    print(VERDE, end='')
                elif (fila, columna) == fin:
                    print(AZUL, end='')
                else:
                    print(AMARILLO, end='')
            else:
                print(tablero[fila][columna], end='')
        print()

def obtener_coordenadas(mensaje, tamaño_tablero):
    while True:
        try:
            x = int(input(f"Introduce la coordenada X, {mensaje}"))
            y = int(input(f"Introduce la coordenada Y, {mensaje}"))
            if 0 <= x < tamaño_tablero and 0 <= y < tamaño_tablero:
                return (x, y)
            else:
                print("Coordenadas fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Introduce números enteros.")

def añadir_obstaculos(tablero, tamaño_tablero, inicio, fin):
    while True:
        coordenadas_obstaculo = input("Escribe 'listo' para terminar o presiona Enter para añadir un obstáculo: ")
        if coordenadas_obstaculo == 'listo':
            break
        try:
            x = int(input("Introduce la coordenada X del obstáculo: "))
            y = int(input("Introduce la coordenada Y del obstáculo: "))
            if 0 <= x < tamaño_tablero and 0 <= y < tamaño_tablero:
                if tablero[x][y] == BLANCO and (x, y) != inicio and (x, y) != fin:
                    tablero[x][y] = ROJO
                    imprimir_mapa(tablero, inicio, fin)
                else:
                    print("Esta celda ya está ocupada o es el inicio/fin. Intenta otra.")
            else:
                print("Coordenadas fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Introduce números enteros.")

def main():
    tamaño_tablero = 5
    tablero = [[BLANCO for _ in range(tamaño_tablero)] for _ in range(tamaño_tablero)]

    inicio = obtener_coordenadas("para el punto de inicio: ", tamaño_tablero)
    imprimir_mapa(tablero, inicio)
    
    fin = obtener_coordenadas("para el punto final: ", tamaño_tablero)
    imprimir_mapa(tablero, inicio, fin)

    añadir_obstaculos(tablero, tamaño_tablero, inicio, fin)

    camino = busqueda(tablero, inicio, fin)

    if camino:
        print("Camino encontrado:")
        imprimir_mapa(tablero, inicio, fin, camino)
    else:
        print("No se encontró un camino.")

main()
