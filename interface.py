import os

import types_structure
import constantes as const
from gestion_stock import trouver_produit

def effacer_ecran_terminal()-> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def demander_nombre(message: str, nb_entier: bool)-> int | float:
    """Renvoie l'entrée utilisateur après l'avoir convertie 
    en entier ou en float"""
    while True:
        reponse = input(message)
        try:
            if nb_entier:
                valeur =  int(reponse)
                if valeur >= 0:
                    return valeur
                else:
                    print(const.CTRL_NB_POSITIF)
            else:
                valeur = float(reponse)
                if valeur >= 0:
                    return valeur
                else:
                    print(const.CTRL_PRIX_VALIDE)
        except ValueError:
            print(const.CTRL_NB_VALIDE)

def demander_info_produit(stock: list[types_structure.Produit]
)-> types_structure.Produit | None:
    """Renvoie un dict Produit (valeurs saisies par l'utilisateur) 
    ou None (si saisie annulée avec nom à vide)"""

    nom = demander_nom_produit(const.LBL_NOM_PRODUIT)
    if nom is None:
        return None
    else:
        prod = trouver_produit(stock, nom)
        if prod is None:
            print(const.INFO_PRODUIT_AJOUTE.format(nom))
        else:
            print(
                const.INFO_VALEUR_ACTU,
                const.INFO_PRODUIT.format(
                    nom,
                    prod[const.CLE_QUANTITE],
                    prod[const.CLE_SEUIL],
                    prod[const.CLE_PRIX]
                ),
                sep=''
            )

        quantite = demander_nombre(const.LBL_QUANTITE_PRODUIT, True)
        seuil = demander_nombre(const.LBL_SEUIL_PRODUIT, True)
        prix = demander_nombre(const.LBL_PRIX_PRODUIT, False)
        return {
            const.CLE_NOM: nom, 
            const.CLE_QUANTITE: quantite, 
            const.CLE_SEUIL: seuil, 
            const.CLE_PRIX: prix
        }

def demander_nom_produit(msg: str)-> str | None:
    while True:
        nom: str = input(msg)
        if nom == "":
            return None
        elif len(nom) > const.LARGEUR_COL:
            print(const.CTRL_NOM_TROP_LONG.format(const.LARGEUR_COL))
        else:
            return nom

def demander_nouveau_nom(stock: list[types_structure.Produit],
                         nom_actuel: str
)-> str | None:
    while True:
        nouveau_nom = demander_nom_produit(const.LBL_NOUVEAU_NOM_PRODUIT)
        if nouveau_nom is None:
            return None
        else:
            if nouveau_nom.lower() == nom_actuel.lower():
                print(const.CTRL_NOM_DIFFERENT.format(nom_actuel))
            else:
                if trouver_produit(stock, nouveau_nom) is None:
                   return nouveau_nom
                else:
                    print(const.CTRL_NOM_EXISTE_DEJA.format(nouveau_nom))

def demander_confirmation_suppression()-> bool:
    while True:
        reponse = input(const.QST_SUPPRESSION)
        match reponse.capitalize():
            case const.CTRL_REP_OUI:
                return True
            case const.CTRL_REP_NON:
                return False
        print(const.CTRL_REP_OUI_NON)

def afficher_noms_colonnes(pour_inventaire: bool = False)-> None:
    if not pour_inventaire:
        largeur_cadre = const.LARGEUR_CADRE
    else:
        largeur_cadre = const.LARGEUR_CADRE_INVENTAIRE 

    print(const.TIRET_CADRE * largeur_cadre)
    if not pour_inventaire:
        print(f"| {const.COL_PRODUIT:{const.LARGEUR_COL}} "
              f"| {const.COL_QUANTITE:>{const.LARGEUR_COL}} "
              f"| {const.COL_SEUIL:>{const.LARGEUR_COL}} |"
        )
    else:
        print(f"| {const.COL_PRODUIT:{const.LARGEUR_COL}} "
              f"| {const.COL_QUANTITE:>{const.LARGEUR_COL}} "
              f"| {const.COL_PRIX:>{const.LARGEUR_COL}} "
              f"| {const.COL_TOTAL:>{const.LARGEUR_COL}} |"
        )
    print(const.TIRET_CADRE * largeur_cadre)

def afficher_stock(stock: list[types_structure.Produit])-> None:
    """Affiche le stock actuel avec quantités et seuils"""
    
    if not stock:
        print(const.INFO_STOCK_VIDE)
    else:
        afficher_noms_colonnes()
        for prod in stock:
            print(f"| {prod[const.CLE_NOM]:{const.LARGEUR_COL}} "
                  f"| {prod[const.CLE_QUANTITE]:>{const.LARGEUR_COL}} "
                  f"| {prod[const.CLE_SEUIL]:>{const.LARGEUR_COL}} |"
            )
        print(const.TIRET_CADRE * const.LARGEUR_CADRE)
    
    input(const.NAV_MSG_TOUCHE_ENTREE_RETOUR_MENU)

def afficher_alertes(alertes: list[types_structure.Produit])-> None:
    """Affiche la liste des noms de produits en dessous du seuil"""

    if not alertes:
        print(const.INFO_AUCUNE_ALERTE)
    else:
        afficher_noms_colonnes()
        for prod in alertes:
            print(f"| {prod[const.CLE_NOM]:{const.LARGEUR_COL}} "
                  f"| {prod[const.CLE_QUANTITE]:>{const.LARGEUR_COL}} "
                  f"| {prod[const.CLE_SEUIL]:>{const.LARGEUR_COL}} |"
            )
        print(const.TIRET_CADRE * const.LARGEUR_CADRE)
    
    input(const.NAV_MSG_TOUCHE_ENTREE_RETOUR_MENU)

def afficher_titre_sous_menu(titre: str, 
                             msg_retour: bool = False, 
                             pour_inventaire: bool = False
)-> None:
    if not pour_inventaire:
        largeur_cadre = const.LARGEUR_CADRE
    else:
        largeur_cadre = const.LARGEUR_CADRE_INVENTAIRE
    print(f"{titre:^{largeur_cadre}}")
    if msg_retour:
        print(f"{const.NAV_MSG_VIDE_RETOUR_MENU:^{largeur_cadre}}\n")

def afficher_info_produit(prod: types_structure.Produit | None)-> None:
    """Affiche les données relatives au produit recherché s'il a été trouvé"""
    if prod is None:
        print(const.INFO_PROD_NON_TROUVE)
    else:
        print(const.INFO_PRODUIT.format(prod[const.CLE_NOM],
                                        prod[const.CLE_QUANTITE],
                                        prod[const.CLE_SEUIL],
                                        prod[const.CLE_PRIX])
        )
        
def afficher_inventaire(stock: list[types_structure.Produit])-> None:
    """Affiche les données relatives à chaque produit ainsi que le montant
    total pour chaque produit et le montant de la totalité du stock
    à la date du jour"""

    if not stock:
        print(const.INFO_STOCK_VIDE)
    else :
        afficher_noms_colonnes(True)
        total_stock = 0.0
        for prod in stock:
            cout_total_prod = prod[const.CLE_QUANTITE] * prod[const.CLE_PRIX]
            print(f"| {prod[const.CLE_NOM]:{const.LARGEUR_COL}} "
                  f"| {prod[const.CLE_QUANTITE]:>{const.LARGEUR_COL}} "
                  f"| {prod[const.CLE_PRIX]:>{const.LARGEUR_COL}.2f} "
                  f"| {cout_total_prod:>{const.LARGEUR_COL}.2f} |"
            )
            total_stock += cout_total_prod
        print(const.TIRET_CADRE * const.LARGEUR_CADRE_INVENTAIRE)
        texte_total_stock = const.INFO_COUT_STOCK.format(total_stock)
        print(f"\n{texte_total_stock:>{const.LARGEUR_CADRE_INVENTAIRE}}")

    input(const.NAV_MSG_TOUCHE_ENTREE_RETOUR_MENU)

def afficher_erreur(code_err: int)-> None:
    match code_err:
        case const.ERR_FILE_NOT_FOUND:
            print(const.ERR_MSG_FICHIER_STOCK_ABSENT)
        case const.ERR_JSON_DECODE_ERROR:
            print(const.ERR_MSG_FICHIER_STOCK_ENDOMMAGE)
            print(const.ERR_MSG_NOUVEAU_FICHIER_STOCK)
            print(const.ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE)
    input(const.NAV_MSG_ENTREE_POUR_CONTINUER)