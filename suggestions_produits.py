from difflib import get_close_matches

import constantes as const
import types_structure
from normalisation import normaliser_chaine_pour_comparaison as norm


def suggerer_produits(
    stock: list[types_structure.Produit],
    nom_recherche: str
) -> list[str]:
    """Renvoie les noms de produits proche du nom recherché"""

    noms_normalises = []
    correspondance_entre_noms = {}

    for produit in stock:
        nom_normalise = norm(produit[const.CLE_NOM])
        nom_reel = produit[const.CLE_NOM]
        noms_normalises.append(nom_normalise)
        correspondance_entre_noms[nom_normalise] = nom_reel

    suggestions = get_close_matches(
        norm(nom_recherche),
        noms_normalises,
        const.RECH_NB_ELEMENTS_RETOUR,
        const.RECH_SEUIL_SIMILARITE
    )
    
    return [
        correspondance_entre_noms[nom_normalise]
        for nom_normalise in suggestions
    ]