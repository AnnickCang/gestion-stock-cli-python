import json
import unicodedata

import types_structure
import constantes as const

def normaliser_pour_tri(chaine: str)-> str:
    """Renvoie une chaîne sans les accents pour le tri alphabétique"""
    chaine_retour = unicodedata.normalize('NFD', chaine.lower())
    chaine_retour = ''.join(c for c in chaine_retour
                            if unicodedata.category(c) != 'Mn')
    return chaine_retour

def trier_stock(stock: list[types_structure.Produit])-> None:
    """Trie le stock par nom de produit"""
    stock.sort(key=lambda item: normaliser_pour_tri(item[const.CLE_NOM]))

def charger_stock()-> tuple[int, list[types_structure.Produit]]:
    try:
        with open(const.FICHIER_STOCK, "r", encoding="utf-8") as f:
            stock = json.load(f)
            for prod in stock:
                prod.setdefault(const.CLE_QUANTITE, 0)
                prod.setdefault(const.CLE_SEUIL, 0)
                prod.setdefault(const.CLE_PRIX, 0.0)
            trier_stock(stock)
            return const.NO_ERR, stock
    except FileNotFoundError:
        return const.ERR_FILE_NOT_FOUND, []
    except json.JSONDecodeError:
        return const.ERR_JSON_DECODE_ERROR, []
    
def sauvegarder_stock(stock: list[types_structure.Produit])-> None:
    trier_stock(stock)
    with open(const.FICHIER_STOCK, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)