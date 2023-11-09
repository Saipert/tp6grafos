class GrafoNoDirigido:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, vertice):
        self.vertices[vertice] = {}

    def agregar_arista(self, vertice1, vertice2, peso):
        self.vertices[vertice1][vertice2] = peso
        self.vertices[vertice2][vertice1] = peso

    def obtener_arbol_expansion_minima(self):
        arbol_expansion_minima = GrafoNoDirigido()
        visitados = set()
        primer_vertice = next(iter(self.vertices))

        visitados.add(primer_vertice)
        while len(visitados) < len(self.vertices):
            menor_peso, nueva_arista = float('inf'), None
            for vertice in visitados:
                for vecino, peso in self.vertices[vertice].items():
                    if vecino not in visitados and peso < menor_peso:
                        menor_peso, nueva_arista = peso, (vertice, vecino, peso)

            if nueva_arista:
                arbol_expansion_minima.agregar_vertice(nueva_arista[0])
                arbol_expansion_minima.agregar_vertice(nueva_arista[1])
                arbol_expansion_minima.agregar_arista(nueva_arista[0], nueva_arista[1], nueva_arista[2])
                visitados.add(nueva_arista[1])

        return arbol_expansion_minima

    def obtener_longitud_cables(self):
        return sum(peso for vertices in self.obtener_arbol_expansion_minima().vertices.values() for peso in vertices.values()) // 2

    def camino_mas_corto(self, inicio, fin):
        distancias, visitados = {vertice: float('inf') for vertice in self.vertices}, set()
        distancias[inicio] = 0

        while visitados != set(self.vertices):
            vertice_actual = min((v for v in self.vertices if v not in visitados), key=lambda x: distancias[x])
            visitados.add(vertice_actual)

            for vecino, peso in self.vertices[vertice_actual].items():
                if distancias[vertice_actual] + peso < distancias[vecino]:
                    distancias[vecino] = distancias[vertice_actual] + peso

        camino = [fin]
        while camino[-1] != inicio:
            vecino_anterior = min(self.vertices[camino[-1]], key=lambda x: distancias[x])
            camino.append(vecino_anterior)

        return list(reversed(camino))

grafo = GrafoNoDirigido()

ambientes = ["cocina", "comedor", "cochera", "quincho", "baño1", "baño2", "habitacion1", "habitacion2", "sala_estar", "terraza", "patio"]
for ambiente in ambientes:
    grafo.agregar_vertice(ambiente)

aristas = [
    ("cocina", "comedor", 5),
    ("cocina", "cochera", 7),
    ("comedor", "quincho", 3),
    ("cochera", "baño1", 4),
    ("baño1", "habitacion1", 2),
    ("habitacion1", "habitacion2", 5),
    ("habitacion2", "sala_estar", 6),
    ("sala_estar", "terraza", 4),
    ("terraza", "patio", 3),
    ("quincho", "baño2", 5),
    ("baño2", "sala_estar", 3),
]

for arista in aristas:
    grafo.agregar_arista(*arista)

arbol_expansion_minima = grafo.obtener_arbol_expansion_minima()
longitud_cables = grafo.obtener_longitud_cables()

print("Árbol de expansión mínima:", arbol_expansion_minima.vertices)
print("Metros de cables necesarios:", longitud_cables)

camino_corto = grafo.camino_mas_corto("habitacion1", "sala_estar")
metros_cable_red = sum(grafo.vertices[camino_corto[i]][camino_corto[i + 1]] for i in range(len(camino_corto) - 1))

print("Camino más corto:", camino_corto)
print("Metros de cable de red necesarios:", metros_cable_red)
