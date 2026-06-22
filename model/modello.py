import copy
import itertools

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.percorso = []
        self.punteggio = 0

    def get_all_years(self):
        return DAO.get_all_years()

    def get_all_shapes(self, anno):
        return DAO.get_all_shapes(anno)

    def crea_grafo(self, anno, forma):
        self._grafo.clear()

        self._grafo.add_nodes_from(DAO.get_all_nodes(anno, forma))

        for a, b in itertools.combinations(self._grafo.nodes, 2):
            if a.state == b.state:
                if a.longitude > b.longitude:
                    self._grafo.add_edge(b, a, weight = abs(a.longitude - b.longitude))
                elif a.longitude < b.longitude:
                    self._grafo.add_edge(a, b, weight = abs(b.longitude - a.longitude))

    def archi_maggiore(self):
        lista = [(a, b, self._grafo[a][b]["weight"]) for a,b in self._grafo.edges]
        lista.sort(key=lambda x : x[2], reverse=True)
        if len(lista) > 4:
            return lista[0:5]
        else:
            return lista


    def dim_grafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_percorso(self):
        self.percorso = []
        self.punteggio = 0
        for n in self._grafo.nodes:
            self._ricorsione([n], 100)

        return self.percorso, self.punteggio

    def _ricorsione(self, parziale, punti):
        if self.punteggio < punti:
            self.punteggio = punti
            self.percorso = copy.deepcopy(parziale)

        for n in self._grafo.successors(parziale[-1]):
            if self._controllo_step(parziale, n):
                x = 100
                if parziale[-1].datetime.month == n.datetime.month:
                    x = 200
                parziale.append(n)
                self._ricorsione(parziale, punti + x)
                parziale.pop()

    def _controllo_step(self, parziale, n):
        if parziale[-1].duration >= n.duration:
            return False

        mese = 0
        for a in parziale:
            if a.datetime.month == n.datetime.month:
                mese += 1

        if mese == 3:
            return False

        return True
