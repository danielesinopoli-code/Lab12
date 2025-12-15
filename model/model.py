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
    def get_shortest_path(self, soglia):
        path_migliores = []
        min_total_weight = float('inf')
        for n in self.G.nodes():
            vicini_validi =[]
            for vicino in self.G.neighbors(n):
                peso=self.G[n][vicino]['weight']
                if peso > soglia:
                    vicini_validi.append((vicino, peso))
            if len(vicini_validi) >=2 : #valido che gli archi siano almeno 2
                vicini_validi.sort(key=lambda x: x[1])
                v1, p1= vicini_validi[0]
                v2, p2= vicini_validi[1]



                peso_attuale= p1 + p2

                if peso_attuale < min_total_weight:
                    min_total_weight = peso_attuale
                    if v1<v2:   #correggo l'ordine degli archi
                        path_migliores= [(v1,n, p1),(n,v2, p2)]
                    else:
                        path_migliores= [(v2,n, p2),(n,v1, p1)]

        return path_migliores, min_total_weight

