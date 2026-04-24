from typing import TypedDict

class Produit(TypedDict):
    nom: str
    quantite: int
    seuil: int
    prix: float