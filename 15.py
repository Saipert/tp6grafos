class GrafoNoDirigido:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, nombre, pais, tipo):
        if nombre not in self.vertices:
            self.vertices[nombre] = {"pais": pais, "tipo": tipo, "conexiones": {}}

    def agregar_arista(self, maravilla1, maravilla2, distancia):
        self.vertices[maravilla1]["conexiones"][maravilla2] = distancia
        self.vertices[maravilla2]["conexiones"][maravilla1] = distancia

    def obtener_arbol_expansion_minima(self, tipo):
        arbol_expansion_minima = GrafoNoDirigido()
        visitados = set()
        primer_maravilla = next(m for m, info in self.vertices.items() if info["tipo"] == tipo)

        visitados.add(primer_maravilla)
        while len(visitados) < sum(1 for info in self.vertices.values() if info["tipo"] == tipo):
            menor_distancia, nueva_arista = float('inf'), None
            for maravilla in visitados:
                for vecino, distancia in self.vertices[maravilla]["conexiones"].items():
                    if vecino not in visitados and distancia < menor_distancia and self.vertices[vecino]["tipo"] == tipo:
                        menor_distancia, nueva_arista = distancia, (maravilla, vecino, distancia)

            if nueva_arista:
                arbol_expansion_minima.agregar_vertice(nueva_arista[0], self.vertices[nueva_arista[0]]["pais"], tipo)
                arbol_expansion_minima.agregar_vertice(nueva_arista[1], self.vertices[nueva_arista[1]]["pais"], tipo)
                arbol_expansion_minima.agregar_arista(nueva_arista[0], nueva_arista[1], nueva_arista[2])
                visitados.add(nueva_arista[1])

        return arbol_expansion_minima

    def paises_con_maravillas(self, tipo):
        paises = set()
        for maravilla, info in self.vertices.items():
            if info["tipo"] == tipo:
                if isinstance(info["pais"], list):
                    paises.update(info["pais"])
                else:
                    paises.add(info["pais"])
        return list(paises)

    def paises_con_mas_de_una_maravilla(self, tipo):
        maravillas_por_pais = {}
        for maravilla, info in self.vertices.items():
            if info["tipo"] == tipo:
                if isinstance(info["pais"], list):
                    for pais in info["pais"]:
                        maravillas_por_pais[pais] = maravillas_por_pais.get(pais, 0) + 1
                else:
                    maravillas_por_pais[info["pais"]] = maravillas_por_pais.get(info["pais"], 0) + 1

        return [pais for pais, cantidad in maravillas_por_pais.items() if cantidad > 1]

    def paises_con_maravillas_arquitectonicas_y_naturales(self):
        paises_arquitectonicas = set(self.paises_con_maravillas("arquitectonica"))
        paises_naturales = set(self.paises_con_maravillas("natural"))
        return list(paises_arquitectonicas.intersection(paises_naturales))

maravillas = GrafoNoDirigido()

maravillas.agregar_vertice("Machu Picchu", "Perú", "arquitectonica")
maravillas.agregar_vertice("Chichén Itzá", "México", "arquitectonica")
maravillas.agregar_vertice("Coliseo", "Italia", "arquitectonica")
maravillas.agregar_vertice("Cristo Redentor", "Brasil", "arquitectonica")
maravillas.agregar_vertice("Gran Muralla China", "China", "arquitectonica")
maravillas.agregar_vertice("Petra", "Jordania", "arquitectonica")
maravillas.agregar_vertice("Estatua de la Libertad", "Estados Unidos", "arquitectonica")

maravillas.agregar_vertice("Iguazú", "Argentina", "natural")
maravillas.agregar_vertice("Amazonas", ["Brasil", "Perú", "Colombia"], "natural")
maravillas.agregar_vertice("Bahía de Ha-Long", "Vietnam", "natural")
maravillas.agregar_vertice("Cataratas del Niágara", ["Estados Unidos", "Canadá"], "natural")
maravillas.agregar_vertice("Montaña de la Mesa", "Sudáfrica", "natural")
maravillas.agregar_vertice("Parque Nacional de Komodo", "Indonesia", "natural")
maravillas.agregar_vertice("Gran Barrera de Coral", "Australia", "natural")

maravillas.agregar_arista("Machu Picchu", "Chichén Itzá", 3)
maravillas.agregar_arista("Chichén Itzá", "Coliseo", 5)
maravillas.agregar_arista("Coliseo", "Cristo Redentor", 2)
maravillas.agregar_arista("Cristo Redentor", "Gran Muralla China", 7)
maravillas.agregar_arista("Gran Muralla China", "Petra", 4)
maravillas.agregar_arista("Petra", "Estatua de la Libertad", 6)
maravillas.agregar_arista("Estatua de la Libertad", "Machu Picchu", 8)

maravillas.agregar_arista("Iguazú", "Amazonas", 2)
maravillas.agregar_arista("Amazonas", "Bahía de Ha-Long", 4)
maravillas.agregar_arista("Bahía de Ha-Long", "Cataratas del Niágara", 3)
maravillas.agregar_arista("Cataratas del Niágara", "Montaña de la Mesa", 5)
maravillas.agregar_arista("Montaña de la Mesa", "Parque Nacional de Komodo", 6)
maravillas.agregar_arista("Parque Nacional de Komodo", "Gran Barrera de Coral", 4)
maravillas.agregar_arista("Gran Barrera de Coral", "Iguazú", 7)

arbol_expansion_minima_arquitectonicas = maravillas.obtener_arbol_expansion_minima("arquitectonica")
arbol_expansion_minima_naturales = maravillas.obtener_arbol_expansion_minima("natural")

paises_con_maravillas_arquitectonicas_y_naturales = maravillas.paises_con_maravillas_arquitectonicas_y_naturales()

paises_con_mas_de_una_maravilla = maravillas.paises_con_mas_de_una_maravilla("arquitectonica") + maravillas.paises_con_mas_de_una_maravilla("natural")

paises_con_mas_de_una_maravilla_total = set(paises_con_mas_de_una_maravilla)

paises_con_mas_de_una_maravilla_arquitectonica_o_natural = maravillas.paises_con_mas_de_una_maravilla("arquitectonica") + maravillas.paises_con_mas_de_una_maravilla("natural")
paises_con_mas_de_una_maravilla_arquitectonica_o_natural = set(paises_con_mas_de_una_maravilla_arquitectonica_o_natural)

print("Árbol de expansión mínima de maravillas arquitectónicas:", arbol_expansion_minima_arquitectonicas.vertices)
print("Árbol de expansión mínima de maravillas naturales:", arbol_expansion_minima_naturales.vertices)

print("Países con maravillas arquitectónicas y naturales:", paises_con_maravillas_arquitectonicas_y_naturales)
print("Países con más de una maravilla arquitectónica o natural:", list(paises_con_mas_de_una_maravilla_total))
