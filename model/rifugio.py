from dataclasses import dataclass


@dataclass
class Rifugio:
    id: int
    nome :str
    localita : str
    altitudine : int
    capienza : int
    aperto : bool


    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.nome
