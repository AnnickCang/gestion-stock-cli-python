from datetime import datetime

import constantes as const
import interface as ifc
import gestion_stock as gs
import donnees

def main():
    retour = donnees.charger_stock()
    code_err = retour[0]
    stock = retour[1]

    if code_err != const.NO_ERR:
        ifc.afficher_erreur(code_err)

    continuer = True
    while continuer:
        ifc.effacer_ecran_terminal()
        print(f"{const.TITRE_MENU_PRINCIPAL:^{const.LARGEUR_CADRE}}\n")
        print(const.MENUP_SM_STOCK)
        print(const.MENUP_SM_ALERTES)
        print(const.MENUP_SM_AJOUT_MODIF)
        print(const.MENUP_SM_SUPPRESSION)
        print(const.MENUP_SM_RECHERCHE)
        print(const.MENUP_SM_RENOMMAGE)
        print(const.MENUP_SM_INVENTAIRE)
        print(const.MENUP_SM_QUITTER)

        choix = input(const.MENUP_CHOIX)

        while choix not in const.LISTE_CHOIX:
            choix = input(const.MENUP_REPETER_CHOIX)

        ifc.effacer_ecran_terminal()
        match choix.capitalize():
            case const.MENUP_CHOIX_STOCK:
                ifc.afficher_titre_sous_menu(const.TITRE_SMENU_STOCK)
                ifc.afficher_stock(stock)
            case const.MENUP_CHOIX_ALERTES:
                 ifc.afficher_titre_sous_menu(
                     const.TITRE_SMENU_ALERTES)
                 alertes = gs.trouver_alertes(stock)
                 ifc.afficher_alertes(alertes)
            case const.MENUP_CHOIX_AJOUT_MODIF:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_AJOUT_MODIF, True)
                    donnees_produit =  ifc.demander_info_produit(stock)
                    if donnees_produit is None:
                        break
                    else:
                        if gs.ajouter_ou_modifier_produit(stock, 
                                                          **donnees_produit
                        ) == const.RETOUR_AJOUT:
                            print(const.INFO_PROD_AJOUTE)
                        else:
                            print(const.INFO_PROD_MODIFIE)
                        print()
            case const.MENUP_CHOIX_SUPPRESSION:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_SUPPRESSION, 
                        True
                    )
                    nom_prod = ifc.demander_nom_produit(const.LBL_NOM_PRODUIT)
                    if nom_prod:
                        prod = gs.trouver_produit(stock, nom_prod)
                        if prod is None:
                            print(const.INFO_PROD_NON_TROUVE)
                        else:
                            if ifc.demander_confirmation_suppression():
                                gs.supprimer_produit(stock, prod)
                                print(const.INFO_PROD_SUPPRIME.format(nom_prod))
                        print()
                    else:
                        break
            case const.MENUP_CHOIX_RECHERCHE:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_RECHERCHE, 
                        True
                    )
                    nom_prod = ifc.demander_nom_produit(const.LBL_NOM_PRODUIT)
                    if nom_prod:
                        prod = gs.trouver_produit(stock, nom_prod)
                        ifc.afficher_info_produit(prod)
                        print()
                    else:
                        break
            case const.MENUP_CHOIX_RENOMMAGE:
                while True:
                    ifc.afficher_titre_sous_menu(
                        const.TITRE_SMENU_RENOMMAGE, 
                        True
                    )
                    nom_prod = ifc.demander_nom_produit(const.LBL_NOM_PRODUIT)
                    if nom_prod:
                        prod = gs.trouver_produit(stock, nom_prod)
                        if prod is None:
                            print(const.INFO_PROD_NON_TROUVE)
                        else:
                            nouveau_nom = ifc.demander_nouveau_nom(
                                stock, 
                                nom_prod
                            )
                            if nouveau_nom is None:
                                break
                            else:
                                gs.renommer_produit(stock, prod, nouveau_nom)
                                print(const.INFO_PROD_RENOMME.format(
                                    nom_prod, 
                                    nouveau_nom
                                    )
                                )
                        print()
                    else:
                        break
            case const.MENUP_CHOIX_INVENTAIRE:
                jour = datetime.today().strftime("%d/%m/%Y")
                titre = const.TITRE_SMENU_INVENTAIRE + jour + " ---"
                ifc.afficher_titre_sous_menu(titre, pour_inventaire=True)
                ifc.afficher_inventaire(stock)
            case const.MENUP_CHOIX_QUITTER:
                continuer = False                

if __name__ == "__main__":
    main()