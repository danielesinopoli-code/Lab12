import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    def handle_path(self,e):
        try:
            soglia = float(self._view.txt_soglia.value)
        except ValueError:
            self._view.show_alert("Inserisci un numero valido per la soglia.")

        self._view.lista_visualizzazione_3.controls.clear()
        path, peso_totale= self._model.get_shortest_path(soglia)

        if not path:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"Nessun cammino trovato con soglia {soglia} e almeno 2 archi.")
            )
            self._view.page.update()
            return

        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Peso totale: {peso_totale:.2f}"))

        for u,v, peso in path:
            nodo_u= self._model.rifugi[u]
            nodo_v= self._model.rifugi[v]

            row= ft.Text(f"[{nodo_u.id}] {nodo_u.nome} -> [{nodo_v.id}] {nodo_v.nome} | peso : {peso:.2f}")
            self._view.lista_visualizzazione_3.controls.append(row)
        self._view.page.update()


