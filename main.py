from typing import Tuple, List, Dict
import pdb

# ## implementación de grafo como lista enlazada.
# las aristas tienen un valor entero (el del vértice) y uno flotante
# (su peso).
Arista = Tuple[int, float]

# los vértices tienen un valor y una lista de artistas.
Vertice = Tuple[int, List[Arista]]


# los grafos se implementan como una lista de vértices,
# con sus repectivos métodos.
class Grafo():
    def __init__(self):
        self.vertices = []

    def __str__(self):
        cadena = []
        for vtr in self.vertices:
            cadena.append("(").append(str(vtr[0])).append(") -> ")
            for ars in vtr[1]:
                cadena.append(
                    str(ars[0])).append(": ").append(str(ars[1]), " - ")
            cadena.append("\n")
        return "".join(map(lambda x: str(x), cadena))

    def agr_vrt(self, vrt: int):
        if vrt not in [x[0] for x in self.vertices]:
            self.vertices.append((vrt, []))

    def elim_vrt(self, vrt: int):
        for vertex in self.vertices:
            vertex = (vertex[0],
                      list(filter(lambda x: x[0] != vrt, vertex[1])))

        self.vertices = list(filter(lambda x: x[0] != vrt, self.vertices))

    def agr_ars(self, orig: int, dest: int, cost: float):
        for vertex in self.vertices:
            if vertex[0] == orig:
                for arista in vertex[1]:
                    if arista[0] == dest:
                        arista[1] = cost
                        break
                vertex[1].append((dest, cost))
                break
        for vertex in self.vertices:
            if vertex[0] == dest:
                for arista in vertex[1]:
                    if arista[0] == orig:
                        arista[1] = cost
                        break
                vertex[1].append((orig, cost))
                break

    def elim_ars(self, orig: int, dest: int):
        # pdb.set_trace()
        for ind, vertex in enumerate(self.vertices):
            if vertex[0] == orig:
                vertex = (vertex[0], list(
                    filter(lambda x: x[0] != dest, vertex[1])))
                self.vertices[ind] = vertex
                break
        for ind, vertex in enumerate(self.vertices):
            if vertex[0] == dest:
                vertex = (vertex[0], list(
                    filter(lambda x: x[0] != orig, vertex[1])))
                self.vertices[ind] = vertex
                break

    # retorna la lista de aristas con los que conecta el vértice
    # dado.
    def aristas(self, vrt: int) -> List[Arista]:
        for vertex in self.vertices:
            if vertex[0] == vrt:
                return vertex[1]
        return []

    # retorna el recorrido del grafo, a partir de un nodo de inicio,
    # siguiendo el orden por profundidad.
    def DFS(self, orig: int) -> List[int]:
        recorrido: List[int] = []
        stack: List[int] = []

        # se agrega el elemento de partida
        stack = [orig] + stack

        # mientras haya elementos en el stack:
        while stack != []:
            # se saca el primero
            current = stack[0]
            stack = stack[1:]

            # se añade, si aún no está, a la lista de visitados
            if current not in recorrido:
                recorrido.append(current)

                # cada nodo que tenga una conexión con este,
                # y no ha sido visitado, se agrega al stack.
                for vrt in self.aristas(current):
                    if vrt[0] not in stack:
                        stack = [vrt[0]] + stack

        return recorrido


# retorna el árbol de expansión mínimo para un grafo, empleando el
# algoritmo de Kruskal.
def Kruskal(graph: Grafo) -> Grafo:
    # se crea un nuevo grafo y se insertan todos los vértices en él,
    # sin los aristas.
    spanning = Grafo()
    for vrt in graph.vertices:
        spanning.agr_vrt(vrt)

    # se agregan todos los aristas en una lista, y se ordena
    # de menor a mayor.
    aristas: List[Tuple[int, int, int]] = []
    for vrt in graph.vertices:
        for ars in vrt[1]:
            aristas.append((vrt[0], ars[0], ars[1]))
    aristas.sort(key=lambda x: x[2])

    # Mientras haya elementos en la lista de aristas:
    for aris in aristas:
        # si la arista conecta dos elementos que estaban inconexos:
        if aris[1] not in graph.DFS(aris[0]):
            # se agrega al grafo final
            spanning.agr_ars(aris[0], aris[1], aris[2])

    return spanning


# retorna una lista de vértices del grafo, más el costo
# de llegar a ellos desde el nodo dado, usando el algoritmo
# de Dijkstra.
def Dijkstra(graph: Grafo, vrt: int) -> Dict[int, float]:
    # si el vértice dado no está en el grafo,
    # se aborta la función
    if vrt not in [x[0] for x in graph.vertices]:
        raise ValueError("El vértice no existe en el grafo")

    # se crea la lista de salida, y se inserta el primer vértice.
    costs = {}
    costs[vrt] = 0.0

    # se crea una lista con los aristas salientes.
    # se inicializa con los aristas del nodo principal.
    outgoing: List[Tuple[int, int, float]] = []
    for arista in graph.aristas(vrt):
        outgoing.append((vrt, arista[0], arista[1]))

    # se crea una lista con los vértices que no han sido agregados.
    # se incluye también el costo tentativo de viaje.
    fuera: Dict[int, float] = {}
    for vertex in graph.vertices[1:]:
        fuera[vertex[0]] = float("inf")

    # mientras la lista de vértices por fuera no esté vacía,
    # y haya al menos un costo no infinito:
    while fuera != [] and filter(
            lambda y: y < float("inf"), [x for x in fuera.values()]) != []:
        # por cada camino que salga del grafo, se compara con el costo
        # actual de dicho nodo. Si es menor, se actualiza. Si no, se deja
        # igual.
        for (orig, dest, cost) in outgoing:
            if costs[orig] + cost < fuera[dest]:
                fuera[dest] = costs[orig] + cost

        # El nodo con (finito) menor costo se agrega a la lista de valores
        # definitivos.
        defin = min(fuera)
        costs[defin] = fuera[defin]

        # Sus demás aristas se agregan a la lista de
        # aristas externos.
        for ari in graph.aristas(defin):
            if ari[0] in fuera.keys():
                outgoing.append((defin, ari[0], ari[1]))
            pass

        # Se borra también de la "lista de espera", y el arista
        # que lo conectaba a los definitivos se elimina de la otra lista
        # (ahora es interno).
        del fuera[defin]
        for ars in outgoing:
            if ars[1] == defin:
                del ars

    return costs


# -- -- -- -- --
# -- -- -- -- --
# ## secuencia principal del programa.
if __name__ == "__main__":
    print("Bienvenido al programa.")
