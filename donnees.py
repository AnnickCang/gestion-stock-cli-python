import json
import errno
import os
from enum import Enum, unique, auto
from typing import NamedTuple

import types_structure as ts
import constantes as const
from normalisation import normaliser_chaine_pour_comparaison as norm


@unique
class ResultatChargementFichier(Enum):
    SUCCES = auto()
    FICHIER_INTROUVABLE = auto()
    JSON_INVALIDE = auto()
    STOCK_PAS_UNE_LISTE = auto()
    ACCES_FICHIER_REFUSE = auto()

@unique
class ResultatSauvegardeFichier(Enum):
    SUCCES = auto()
    ANNULATION = auto()
    ACCES_FICHIER_REFUSE = auto()
    ERREUR_ECRITURE = auto()
    DONNEES_NON_SERIALISABLES = auto()

class ResultatChargementStock(NamedTuple):
    resultat_chargement: ResultatChargementFichier
    stock: list[ts.Produit]
    produits_avec_anomalies: list[ts.ProduitAvecAnomalies]


ERREURS_ECRITURE_PREVISIBLES = {
    errno.ENOSPC,
    errno.EIO,
    errno.EROFS,
    errno.EFBIG
}


CLE_NOM = const.CLE_NOM
CLE_QUANTITE = const.CLE_QUANTITE
CLE_SEUIL = const.CLE_SEUIL
CLE_PRIX = const.CLE_PRIX


def _supprimer_fichier_temp() -> None:
    try:
        os.remove(const.FICHIER_STOCK_TEMP)
    except OSError:
        pass


def _verifier_structure_stock(stock: object) -> ResultatChargementFichier:
    """Renvoie un code indiquant si la structure est valide ou pas"""
    if not isinstance(stock, list):
        return ResultatChargementFichier.STOCK_PAS_UNE_LISTE
    
    return ResultatChargementFichier.SUCCES


def _extraire_champ_entier_valide(
    produit: dict[str, object],
    champ: str
) -> ts.EntierExtraitAvecWarning:
    """Vérifie et renvoie un entier >= 0 avec éventuellement un warning"""

    entier_valide = 0

    msg_champ_inexistant = const.ANO_CHAMP_NUM_INEXISTANT.format(champ)
    msg_converti_a_zero = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
    msg_converti_en_entier = const.ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT.format(
        champ,
        const.ANO_ENTIER
    )

    if champ not in produit:
        return ts.EntierExtraitAvecWarning(entier_valide, msg_champ_inexistant)
    
    valeur_champ = produit[champ]

    if isinstance(valeur_champ, int):
        if isinstance(valeur_champ, bool) or valeur_champ < 0:
            return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_a_zero)
        
        valeur = valeur_champ
        return ts.EntierExtraitAvecWarning(valeur, "")
    
    if isinstance(valeur_champ, float):
        if valeur_champ < 0:
            return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_a_zero)
        
        entier_valide = int(valeur_champ)
        return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_en_entier)
    
    if isinstance(valeur_champ, str):
        try:
            valeur_convertie = float(valeur_champ)
            valeur_convertie = int(valeur_convertie)

            if valeur_convertie < 0:
                return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_a_zero)

            entier_valide = valeur_convertie
            msg_converti_en_nombre = const.ANO_CHAMP_NUM_CONV_VAL.format(
                champ,
                entier_valide
            )
            return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_en_nombre)

        except ValueError:
            return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_a_zero)

    return ts.EntierExtraitAvecWarning(entier_valide, msg_converti_a_zero)


def _extraire_champ_flottant_valide(
    produit: dict[str, object],
    champ: str
) -> ts.FlottantExtraitAvecWarning:
    """Vérifie et renvoie un flottant >= 0 avec éventuellement un warning"""

    flottant_valide = 0.0

    msg_champ_inexistant = const.ANO_CHAMP_NUM_INEXISTANT.format(champ)
    msg_converti_a_zero = const.ANO_CHAMP_NUM_CONV_ZERO.format(champ)
    msg_converti_en_flottant = const.ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT.format(
        champ,
        const.ANO_FLOTTANT
    )

    if champ not in produit:
        return ts.FlottantExtraitAvecWarning(flottant_valide, msg_champ_inexistant)
    
    valeur_champ = produit[champ]

    if isinstance(valeur_champ, float):
        if valeur_champ < 0:
            return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_a_zero)
        
        flottant_valide = valeur_champ
        return ts.FlottantExtraitAvecWarning(flottant_valide, "")
    
    if isinstance(valeur_champ, int):
        if isinstance(valeur_champ, bool) or valeur_champ < 0:
            return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_a_zero)
        
        flottant_valide = float(valeur_champ)
        return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_en_flottant)
    
    if isinstance(valeur_champ, str):
        try:
            valeur_convertie = float(valeur_champ)

            if valeur_convertie < 0:
                return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_a_zero)

            flottant_valide = valeur_convertie
            msg_converti_en_nombre = const.ANO_CHAMP_NUM_CONV_VAL.format(
                champ,
                flottant_valide
            )
            return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_en_nombre)

        except ValueError:
            return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_a_zero)
    
    return ts.FlottantExtraitAvecWarning(flottant_valide, msg_converti_a_zero)


def _extraire_nom_produit_valide(
    produit: dict[str, object]
) -> ts.NomExtraitAvecWarnings:
    """Vérifie et renvoie un nom valide ou None avec la liste des warnings associés"""
    
    taille_max_nom_produit = const.TAILLE_MAX_NOM_PRODUIT

    anomalies_nom = []
    
    if CLE_NOM not in produit:
        anomalies_nom.append(const.ANO_NOM_INEXISTANT)
        return ts.NomExtraitAvecWarnings(None, anomalies_nom)
    
    nom = produit[CLE_NOM]
    if not isinstance(nom, str):
        anomalies_nom.append(const.ANO_CHAMP_PAS_STR.format(CLE_NOM))
        return ts.NomExtraitAvecWarnings(None, anomalies_nom)
    
    nom_strip = nom.strip()
    if nom_strip == "":
        anomalies_nom.append(const.ANO_NOM_VIDE.format(CLE_NOM))
        return ts.NomExtraitAvecWarnings(None, anomalies_nom)
        
    if len(nom_strip) > taille_max_nom_produit:
        nom_strip = nom_strip[:taille_max_nom_produit]
        anomalies_nom.append(
            const.ANO_CHAMP_TROP_LONG.format(CLE_NOM, taille_max_nom_produit)
        )
    
    return ts.NomExtraitAvecWarnings(nom_strip, anomalies_nom)


def _extraire_champs_numeriques_valides(
    produit: dict[str, object]
) -> ts.ChampsNumeriquesExtraitsAvecWarnings:
    """Vérifie et renvoie les champs numériques avec une valeur valide ou 0
    et la liste des warnings associés"""
    
    champs_numeriques_anomalies = []

    quantite, msg_anomalie = _extraire_champ_entier_valide(produit, CLE_QUANTITE)
    if msg_anomalie != "":
        champs_numeriques_anomalies.append(msg_anomalie)
    seuil, msg_anomalie = _extraire_champ_entier_valide(produit, CLE_SEUIL)
    if msg_anomalie != "":
        champs_numeriques_anomalies.append(msg_anomalie)
    prix, msg_anomalie = _extraire_champ_flottant_valide(produit, CLE_PRIX)
    if msg_anomalie != "":
        champs_numeriques_anomalies.append(msg_anomalie)

    champs_numeriques_produit: ts.ChampsNumeriquesProduit = {
        CLE_QUANTITE: quantite,
        CLE_SEUIL: seuil,
        CLE_PRIX: prix
    }
    return ts.ChampsNumeriquesExtraitsAvecWarnings(
        champs_numeriques_produit,
        champs_numeriques_anomalies
    )


def _extraire_produit_valide(
    produit: object
) -> ts.ProduitExtraitValideAvecWarnings:
    """Vérifie et retourne un produit avec des clés et valeurs valides ou None
    et la liste de warnings associés"""
    
    produit_anomalies = []

    if not isinstance(produit, dict):
        produit_anomalies.append(const.ANO_PRODUIT_STRUCTURE_INVALIDE)
        return ts.ProduitExtraitValideAvecWarnings(None, produit_anomalies)
     
    produit_dict: dict[str, object] = produit
    nom_nettoye, nom_anomalies = _extraire_nom_produit_valide(produit_dict)
    produit_anomalies.extend(nom_anomalies)
    if nom_nettoye is None:
        return ts.ProduitExtraitValideAvecWarnings(None, produit_anomalies)
    
    numeriques_valides, anomalies_numeriques = _extraire_champs_numeriques_valides(produit_dict)
    produit_anomalies.extend(anomalies_numeriques)
    
    produit_nettoye: ts.Produit = {
        CLE_NOM: nom_nettoye,
        CLE_QUANTITE: numeriques_valides[CLE_QUANTITE],
        CLE_SEUIL: numeriques_valides[CLE_SEUIL],
        CLE_PRIX: numeriques_valides[CLE_PRIX]
    }
    return ts.ProduitExtraitValideAvecWarnings(produit_nettoye, produit_anomalies)


def _extraire_stock_valide(
    stock: list[object]
) -> ts.ResultatExtractionStock:
    """Renvoie un stock avec des produits vérifiés, nettoyés et sans doublons
    et éventuellement les anomalies associées"""

    stock_nettoye: list[ts.Produit] = []
    produits_avec_anomalies: list[ts.ProduitAvecAnomalies] = []
    cles_noms_deja_vus: set[str] = set()

    for no_produit, produit in enumerate(stock, start=1):
        produit_nettoye, msgs_anomalies = _extraire_produit_valide(produit)
        
        if produit_nettoye is not None:
            nom_normalise = norm(produit_nettoye[CLE_NOM])
            if nom_normalise in cles_noms_deja_vus:
                msg_anomalie = const.ANO_NOM_DOUBLON.format(produit_nettoye[CLE_NOM])
                msgs_anomalies.append(msg_anomalie)
                produit_nettoye = None
            else:
                cles_noms_deja_vus.add(nom_normalise)
                stock_nettoye.append(produit_nettoye)

        if msgs_anomalies:
            produits_avec_anomalies.append(
                ts.ProduitAvecAnomalies(
                    numero=no_produit,
                    produit_original=produit,
                    anomalies=msgs_anomalies,
                    produit_nettoye=produit_nettoye
                )
            )

    return ts.ResultatExtractionStock(stock_nettoye, produits_avec_anomalies)


def trier_stock(stock: list[ts.Produit]) -> None:
    """Trie le stock par nom de produit"""
    stock.sort(key=lambda item: norm(item[CLE_NOM]))


def charger_stock() -> ResultatChargementStock:
    """Charge les données du fichier de stock et renvoie un résultat de chargement,
    la liste des produits valides et la liste des anomalies"""
    try:
        with open(const.FICHIER_STOCK, "r", encoding="utf-8") as f:
            stock = json.load(f)

            resultat_structure = _verifier_structure_stock(stock)
            if resultat_structure is ResultatChargementFichier.STOCK_PAS_UNE_LISTE:
                return ResultatChargementStock(
                    ResultatChargementFichier.STOCK_PAS_UNE_LISTE,
                    [],
                    []
                )

            stock_nettoye, produits_avec_anomalies = _extraire_stock_valide(stock)

            trier_stock(stock_nettoye)

            return ResultatChargementStock(
                ResultatChargementFichier.SUCCES,
                stock_nettoye,
                produits_avec_anomalies
            )
        
    except FileNotFoundError:
        return ResultatChargementStock(
            ResultatChargementFichier.FICHIER_INTROUVABLE,
            [],
            []
        )
    except json.JSONDecodeError:
        return ResultatChargementStock(
            ResultatChargementFichier.JSON_INVALIDE,
            [],
            []
        )
    except PermissionError:
        return ResultatChargementStock(
            ResultatChargementFichier.ACCES_FICHIER_REFUSE,
            [],
            []
        )
    
    
def sauvegarder_stock(stock: list[ts.Produit]) -> ResultatSauvegardeFichier:
    """Sauvegarde le stock trié par nom et renvoie le résultat de la sauvegarde"""
    trier_stock(stock)
    try:
        with open(const.FICHIER_STOCK_TEMP, "w", encoding="utf-8") as f:
            json.dump(stock, f, indent=4, ensure_ascii=False)
        os.replace(const.FICHIER_STOCK_TEMP, const.FICHIER_STOCK)
        return ResultatSauvegardeFichier.SUCCES
    except PermissionError:
        _supprimer_fichier_temp()
        return ResultatSauvegardeFichier.ACCES_FICHIER_REFUSE
    except OSError as erreur:
        _supprimer_fichier_temp()
        if erreur.errno in ERREURS_ECRITURE_PREVISIBLES:
            return ResultatSauvegardeFichier.ERREUR_ECRITURE
        raise
    except TypeError:
        _supprimer_fichier_temp()
        return ResultatSauvegardeFichier.DONNEES_NON_SERIALISABLES