from typing import TypedDict
from typing import NamedTuple
from dataclasses import dataclass


class Produit(TypedDict):
    nom: str
    quantite: int
    seuil: int
    prix: float


class ChampsNumeriquesProduit(TypedDict):
    quantite: int
    seuil: int
    prix: float


class InfosProduitFormatees(NamedTuple):
    nom: str
    quantite: str
    seuil: str
    prix: str


class EntierExtraitAvecWarning(NamedTuple):
    entier: int
    warning: str


class FlottantExtraitAvecWarning(NamedTuple):
    flottant: float
    warning: str


class NomExtraitAvecWarnings(NamedTuple):
    nom: str | None
    warnings: list[str]


class ChampsNumeriquesExtraitsAvecWarnings(NamedTuple):
    champs_numeriques: ChampsNumeriquesProduit
    warnings: list[str]


class ProduitExtraitValideAvecWarnings(NamedTuple):
    produit: Produit | None
    warnings: list[str]


class StockExtraitValideAvecWarnings(NamedTuple):
    stock: list[Produit]
    warnings: list[str]


@dataclass
class ProduitAvecAnomalies:
    numero: int
    produit_original: object
    anomalies: list[str]
    produit_nettoye: Produit | None