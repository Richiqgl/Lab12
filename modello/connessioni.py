from dataclasses import dataclass
@dataclass
class Connessione():
    codiceRetailer1:int
    codiceRetailer2:int
    Conto:int


    def __str__(self):
        return f"{self.codiceRetailer1}---{self.codiceRetailer2}---{self.Conto}"

