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

def verifier_et_nettoyer_produit(prod: types_structure.Produit
)-> tuple[types_structure.Produit | None, list[str]]:
    """Vérifie et retourne un produit avec des clés et valeurs valides ou None
    avec la liste de warnings associés"""
    
    prod_nettoye = None
    anomalies_produit = []

    if const.CLE_NOM not in prod:
        anomalies_produit.append(const.ANO_NOM_INEXISTANTE)
    elif not isinstance(prod[const.CLE_NOM], str):
        anomalies_produit.append(const.ANO_NOM_PAS_STR)
    else:
        nom_strip = prod[const.CLE_NOM].strip()
        if nom_strip == "":
            anomalies_produit.append(const.ANO_NOM_VIDE)
        else:
            if len(nom_strip) > const.LARGEUR_COL:
                nom_strip = nom_strip[:const.LARGEUR_COL]
                anomalies_produit.append(const.ANO_NOM_TROP_LONG)

            prod_nettoye = {
                const.CLE_NOM: nom_strip,
                const.CLE_QUANTITE: prod[const.CLE_QUANTITE],
                const.CLE_SEUIL: prod[const.CLE_SEUIL],
                const.CLE_PRIX: prod[const.CLE_PRIX]
            }
    
    return prod_nettoye, anomalies_produit

def charger_stock(
)-> tuple[int, list[types_structure.Produit], list[str]]:
    """Charge les données du fichier de stock et renvoie le code erreur ou pas d'erreur,
    la liste des produits valides et la liste des anomalies"""
    try:
        with open(const.FICHIER_STOCK, "r", encoding="utf-8") as f:
            stock = json.load(f)
            stock_nettoye = []
            anomalies = []
            no_prod = 0
            for prod in stock:
                no_prod += 1
                prod.setdefault(const.CLE_QUANTITE, 0)
                prod.setdefault(const.CLE_SEUIL, 0)
                prod.setdefault(const.CLE_PRIX, 0.0)
                prod_nettoye, msgs_anomalies = verifier_et_nettoyer_produit(prod)
                if prod_nettoye is not None:
                    stock_nettoye.append(prod_nettoye)
                for ano in msgs_anomalies:
                    txt_anomalie = const.ANO_NO_PRODUIT.format(no_prod)
                    anomalies.append(txt_anomalie + ano)
            trier_stock(stock_nettoye)
            return const.NO_ERR, stock_nettoye, anomalies
    except FileNotFoundError:
        return const.ERR_FILE_NOT_FOUND, [], []
    except json.JSONDecodeError:
        return const.ERR_JSON_DECODE_ERROR, [], []
    
def sauvegarder_stock(stock: list[types_structure.Produit])-> None:
    trier_stock(stock)
    with open(const.FICHIER_STOCK, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)