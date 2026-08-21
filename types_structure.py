from dataclasses import dataclass
from typing import NamedTuple, TypedDict


class Produit(TypedDict):
    nom: str
    quantite: int
    seuil: int
    prix: float


class ChampsNumeriquesProduit(TypedDict):
    quantite: int
    seuil: int
    prix: float


@dataclass
class ProduitAvecAnomalies:
    """
    Représente un produit ayant présenté une ou plusieurs anomalies
    lors du chargement du stock.
    Si `produit_nettoye` vaut `None`, le produit n'a pas été conservé
    dans le stock nettoyé
    """
    numero: int
    produit_original: object
    anomalies: list[str]
    produit_nettoye: Produit | None


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
    nom_normalise: str | None


class ResultatExtractionStock(NamedTuple):
    stock: list[Produit]
    produits_avec_anomalies: list[ProduitAvecAnomalies]