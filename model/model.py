import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self.rifugi = {}

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()
        lista_rifugi = DAO.get_all_rifugi()
        self.rifugi ={}
        for r in lista_rifugi:
            self.rifugi[r.id] = r

        connessioni= DAO.get_all_connessione_by_year(year)

        for c in connessioni: # aggiungo solo i nodi che hanno una connessione
            u=c.id_rifugio1
            v=c.id_rifugio2

            if not  self.G.has_node(u):
                self.G.add_node(u, data=self.rifugi[u])
            if not self.G.has_node(v):
                self.G.add_node(v, data=self.rifugi[v])

            peso= self._calcola_peso(c.distanza,c.difficolta)
            self.G.add_edge(c.id_rifugio1, c.id_rifugio2, weight=peso, data= c)

    def _calcola_peso(self, distanza, difficolta):
        fattore = 1
        if difficolta == "media":
            fattore = 1.5
        if difficolta == "difficile":
            fattore = 2
        return float(distanza) * fattore




    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        numero_archi=self.G.number_of_edges()

        if numero_archi == 0:
            return 0, 0
        pesi = []

        for u, v ,data in self.G.edges(data=True):
            pesi.append( data['weight'])
        return min(pesi), max(pesi)


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0

        for u,v,data in self.G.edges(data=True):
            if data['weight'] < soglia:
                minori += 1
            elif data['weight'] > soglia:
                maggiori += 1
        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
