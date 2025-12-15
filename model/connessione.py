from dataclasses import dataclass
import datetime

@dataclass
class Connessione:
    id :int
    id_rifugio1 : int
    id_rifugio2 : int
    distanza : float
    difficolta : str
    durata : datetime.timedelta
    anno : int

    def __str__(self):
        return f"{self.id_rifugio1}<->{self.id_rifugio2}"