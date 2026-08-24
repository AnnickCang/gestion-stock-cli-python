import constantes as const
import types_structure
from normalisation import normaliser_chaine_pour_comparaison as norm

CLE_NOM = const.CLE_NOM
CLE_QUANTITE = const.CLE_QUANTITE
CLE_SEUIL = const.CLE_SEUIL
CLE_PRIX = const.CLE_PRIX


def trouver_produit(
    stock: list[types_structure.Produit], 
    nom: str
) -> types_structure.Produit | None:
    """Retourne le produit correspondant au nom normalisé ou None"""
    for produit in stock:
        if norm(produit[CLE_NOM]) == norm(nom):
            return produit
        
    return None


def ajouter_produit(
    stock: list[types_structure.Produit],
    nom: str, 
    quantite: int,
    seuil: int, 
    prix: float,
) -> None:
    produit: types_structure.Produit = {
        CLE_NOM: nom,
        CLE_QUANTITE: quantite,
        CLE_SEUIL: seuil,
        CLE_PRIX: round(prix, 2)
    }
    stock.append(produit)


def modifier_produit(
    produit: types_structure.Produit, 
    quantite: int,
    seuil: int, 
    prix: float,
) -> None:
    produit[CLE_QUANTITE] = quantite
    produit[CLE_SEUIL] = seuil
    produit[CLE_PRIX] = round(prix, 2)


def trouver_alertes(
    stock: list[types_structure.Produit]
) -> list[types_structure.Produit]:
    """Renvoie la liste des produits sous leur seuil d'alerte"""
    return [
        produit
        for produit in stock
        if produit[CLE_QUANTITE] < produit[CLE_SEUIL]
    ]


def supprimer_produit(
    stock: list[types_structure.Produit], 
    produit: types_structure.Produit
) -> None:
    stock.remove(produit)


def renommer_produit(
    produit: types_structure.Produit,
    nouveau_nom: str
) -> None:
    produit[CLE_NOM] = nouveau_nom


def verifier_nom_disponible(
    stock: list[types_structure.Produit],
    ancien_nom: str,
    nouveau_nom: str
) -> bool:
    """Retourne True si le nom est disponible.
    Un nom normalisé identique à celui du produit courant est autorisé
    pour permettre la modification de la casse ou des accents."""

    for produit in stock:
        if norm(ancien_nom) == norm(produit[CLE_NOM]):
            continue
        if norm(nouveau_nom) == norm(produit[CLE_NOM]):
            return False
    
    return True


def verifier_quantite_sous_seuil(produit: types_structure.Produit) -> bool:
    """Renvoie True si la quantité d'un produit est sous le seuil"""
    return produit[CLE_QUANTITE] < produit[CLE_SEUIL]


def verifier_prix_nul(produit: types_structure.Produit) -> bool:
    """Renvoie True si le prix est nul"""
    return produit[CLE_PRIX] == 0