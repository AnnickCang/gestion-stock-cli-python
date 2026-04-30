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

def verifier_champ_numerique(prod: types_structure.Produit,
                             champ: str,
                             type_numerique: str
)-> tuple[int | float, str]:
    """Vérifie et renvoie une valeur correcte (nombre positif ou 0)
    pour un champ numérique avec éventuellement un warning"""
    match type_numerique:
        case const.ANO_ENTIER:
            valeur_defaut = 0
        case const.ANO_FLOTTANT:
            valeur_defaut = 0.0
    valeur = valeur_defaut
    msg = ""

    if champ in prod:
        if isinstance(prod[champ], int | float):
            if isinstance(prod[champ], bool) or prod[champ] < 0:
                msg = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
            elif type_numerique == const.ANO_FLOTTANT and isinstance(
                prod[champ], int):
                valeur = float(prod[champ])
                msg = const.ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT.format(
                    champ, const.ANO_FLOTTANT)
            elif type_numerique == const.ANO_ENTIER and isinstance(
                prod[champ], float):
                valeur = int(prod[champ])
                msg = const.ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT.format(
                    champ, const.ANO_ENTIER)
            else:
                valeur = prod[champ]
        else:
            if isinstance(prod[champ], str):
                try:
                    valeur_temp = float(prod[champ])
                    if type_numerique == const.ANO_ENTIER:
                        valeur_temp = int(valeur_temp)

                    if valeur_temp < 0:
                        msg = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
                    else:
                        valeur = valeur_temp
                        msg = const.ANO_CHAMP_NUM_CONV_VAL.format(champ, valeur)

                except ValueError:
                    msg = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
            else:
                msg = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
    else:
        msg = const.ANO_CHAMP_NUM_INEXISTANT.format(champ)

    return valeur, msg

def verifier_et_nettoyer_produit(prod: types_structure.Produit
)-> tuple[types_structure.Produit | None, list[str]]:
    """Vérifie et retourne un produit avec des clés et valeurs valides ou None
    avec la liste de warnings associés"""
    
    prod_nettoye = None
    anomalies_produit = []

    #Vérification du nom
    if const.CLE_NOM not in prod:
        anomalies_produit.append(const.ANO_NOM_INEXISTANTE)
    elif not isinstance(prod[const.CLE_NOM], str):
        anomalies_produit.append(const.ANO_CHAMP_PAS_STR.format(const.CLE_NOM))
    else:
        nom_strip = prod[const.CLE_NOM].strip()
        if nom_strip == "":
            anomalies_produit.append(
                const.ANO_CHAMP_VIDE.format(const.CLE_NOM))
        else:
            if len(nom_strip) > const.LARGEUR_COL:
                nom_strip = nom_strip[:const.LARGEUR_COL]
                anomalies_produit.append(const.ANO_CHAMP_TROP_LONG.format(
                    const.CLE_NOM, const.LARGEUR_COL))

            #Nom validé - Vérification des champs numériques
            quantite, msg_ano = verifier_champ_numerique(
                prod, const.CLE_QUANTITE, const.ANO_ENTIER)
            if msg_ano != "":
                anomalies_produit.append(msg_ano)
            seuil, msg_ano = verifier_champ_numerique(
                prod, const.CLE_SEUIL, const.ANO_ENTIER)
            if msg_ano != "":
                anomalies_produit.append(msg_ano)
            prix, msg_ano = verifier_champ_numerique(
                prod, const.CLE_PRIX, const.ANO_FLOTTANT)
            if msg_ano != "":
                anomalies_produit.append(msg_ano)

            #Produit validé
            prod_nettoye = {
                const.CLE_NOM: nom_strip,
                const.CLE_QUANTITE: quantite,
                const.CLE_SEUIL: seuil,
                const.CLE_PRIX: prix
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