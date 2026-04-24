import types_structure
import constantes as const
from donnees import sauvegarder_stock

def trouver_produit(stock: list[types_structure.Produit], 
                    nom: str
)-> types_structure.Produit | None:
    """Retourne le produit correspondant au nom donné 
    ou None s'il n'existe pas"""
    for prod in stock:
        if prod[const.CLE_NOM].lower() == nom.lower():
            return prod
    return None

def ajouter_produit(stock: list[types_structure.Produit], 
                    nom: str, 
                    quantite: int, 
                    seuil: int, 
                    prix: float
)-> None:
    """Ajoute un produit au stock"""
    prod = {
        const.CLE_NOM: nom,
        const.CLE_QUANTITE: quantite,
        const.CLE_SEUIL: seuil,
        const.CLE_PRIX: round(prix, 2)
    }
    stock.append(prod)

def ajouter_ou_modifier_produit(stock: list[types_structure.Produit],
                                nom: str, 
                                quantite: int,
                                seuil: int, 
                                prix: float,
)-> int:
    """Ajoute un nouveau produit au stock ou modifie un produit existant"""
    
    prod = trouver_produit(stock, nom)
    if prod is None:
        ajouter_produit(stock, nom, quantite, seuil, prix)
        retour = const.RETOUR_AJOUT
    else:
        prod[const.CLE_QUANTITE] = quantite
        prod[const.CLE_SEUIL] = seuil
        prod[const.CLE_PRIX] = round(prix, 2)
        retour = const.RETOUR_MODIFICATION
    sauvegarder_stock(stock)
    return retour

def trouver_alertes(stock: list[types_structure.Produit]
)-> list[types_structure.Produit]:
    """Renvoie la liste des produits sous leur seuil d'alerte"""
    alertes = []
    for prod in stock:
        if prod[const.CLE_QUANTITE] < prod[const.CLE_SEUIL]:
            alertes.append(prod)
    return alertes

def supprimer_produit(stock: list[types_structure.Produit], 
                      prod: types_structure.Produit
)-> None:
    stock.remove(prod)
    sauvegarder_stock(stock)

def renommer_produit(stock: list[types_structure.Produit],
                     prod: types_structure.Produit,
                     nouveau_nom: str
)-> None:
    prod[const.CLE_NOM] = nouveau_nom
    sauvegarder_stock(stock)