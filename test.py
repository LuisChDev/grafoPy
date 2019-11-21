import unittest
from main import Grafo, Kruskal, Dijkstra


class TestGrafoMethods(unittest.TestCase):
    def test_createGraph(self):
        graf = Grafo()
        graf.agr_vrt(1)
        graf.agr_vrt(2)

        self.assertEqual(graf.vertices[0], (1, []))
        graf.agr_vrt(1)
        self.assertEqual(len(graf.vertices), 2)

    def test_addArchs(self):
        graf = Grafo()
        graf.agr_vrt(1)
        graf.agr_vrt(2)

        graf.agr_ars(1, 2, 3.0)
        self.assertEqual(graf.vertices[0][1][0], (2, 3.0))
        self.assertEqual(graf.vertices[1][1][0], (1, 3.0))

    def test_elimVrt(self):
        graf = Grafo()
        graf.agr_vrt(1)
        graf.agr_vrt(2)

        graf.elim_vrt(1)
        self.assertEqual(graf.vertices[0], (2, []))

    def test_remArchs(self):
        graf = Grafo()
        graf.agr_vrt(1)
        graf.agr_vrt(2)
        graf.agr_ars(1, 2, 3.0)
        self.assertEqual(graf.vertices[0][1][0], (2, 3.0))
        self.assertEqual(graf.vertices[1][1][0], (1, 3.0))

        graf.elim_ars(1, 2)
        self.assertEqual(graf.vertices[0][1], [])
        self.assertEqual(graf.vertices[1][1], [])

    def test_DFS(self):
        graf = Grafo()
        graf.agr_vrt(1)
        graf.agr_vrt(2)
        graf.agr_vrt(3)
        graf.agr_vrt(4)
        graf.agr_vrt(5)  # no lo conectamos
        graf.agr_ars(1, 2, 3.0)
        graf.agr_ars(1, 3, 4.0)
        graf.agr_ars(2, 4, 2.0)

        # self.assertEqual(graf.DFS(1), [1, 2, 4, 3]) # no siempre es así
        self.assertTrue(5 not in graf.DFS(1))
        self.assertTrue(5 not in graf.DFS(3))

    def test_kruskal(self):
        graf = Grafo()
        graf.agr_vrt(1)
        graf.agr_vrt(2)
        graf.agr_vrt(3)
        graf.agr_vrt(4)
        graf.agr_ars(1, 2, 3.0)
        graf.agr_ars(1, 3, 4.0)
        graf.agr_ars(2, 4, 2.0)
        graf.agr_ars(1, 4, 6.0)

        # el arbol no debe contener el camino de 1 a 4

    def test_Dijkstra(self):
        pass


if __name__ == "__main__":
    unittest.main()
