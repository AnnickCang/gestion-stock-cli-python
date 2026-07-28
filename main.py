import types_structure
import constantes as const
import interface as ifc
import gestion_stock as gs
import donnees
import suggestions_produits as sp


LBL_NOM_PRODUIT = const.LBL_NOM_PRODUIT
CLE_NOM = const.CLE_NOM


def _gerer_ajout_modification(
    stock: list[types_structure.Produit]
) -> donnees.ResultatSauvegardeFichier:
    while True:
        ifc.afficher_entete_ajout_modification()

        nom_produit = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_produit is None:
            return donnees.ResultatSauvegardeFichier.ANNULATION
        
        produit = gs.trouver_produit(stock, nom_produit)
        if produit is None:
            donnees_produit = ifc.demander_info_produit(None, nom_produit)
            if donnees_produit is None:
                return donnees.ResultatSauvegardeFichier.ANNULATION

            gs.ajouter_produit(stock, nom_produit, **donnees_produit)
            resultat_sauvegarde = donnees.sauvegarder_stock(stock)
            if resultat_sauvegarde is not donnees.ResultatSauvegardeFichier.SUCCES:
                return resultat_sauvegarde

            ifc.afficher_produit_ajoute(nom_produit)
            continue


        donnees_produit = ifc.demander_info_produit(produit)
        if donnees_produit is None:
            return donnees.ResultatSauvegardeFichier.ANNULATION

        gs.modifier_produit(produit, **donnees_produit)
        resultat_sauvegarde = donnees.sauvegarder_stock(stock)
        if resultat_sauvegarde is not donnees.ResultatSauvegardeFichier.SUCCES:
            return resultat_sauvegarde

        ifc.afficher_produit_modifie(nom_produit)


def _gerer_suppression(
    stock: list[types_structure.Produit]
) -> donnees.ResultatSauvegardeFichier:
    while True:
        ifc.afficher_entete_suppression()

        if not stock:
            ifc.afficher_suppression_impossible()
            return donnees.ResultatSauvegardeFichier.ANNULATION

        nom_produit = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_produit is None:
            return donnees.ResultatSauvegardeFichier.ANNULATION
        
        produit = gs.trouver_produit(stock, nom_produit)
        if produit is None:
            ifc.afficher_produit_non_trouve(nom_produit)
            continue

        nom_produit_a_supprimer = produit[CLE_NOM]
        if ifc.demander_confirmation_suppression(nom_produit_a_supprimer):
            gs.supprimer_produit(stock, produit)
            resultat_sauvegarde = donnees.sauvegarder_stock(stock)
            if resultat_sauvegarde is not donnees.ResultatSauvegardeFichier.SUCCES:
                return resultat_sauvegarde

            ifc.afficher_produit_supprime(nom_produit_a_supprimer)


def _gerer_recherche(stock: list[types_structure.Produit]) -> None:
    while True:
        ifc.afficher_entete_recherche()

        if not stock:
            ifc.afficher_recherche_impossible()
            break

        nom_recherche = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_recherche is None:
            break
        
        produit = gs.trouver_produit(stock, nom_recherche)
        if produit is not None:
            ifc.afficher_info_produit(produit)
            continue

        suggestions = sp.suggerer_produits(stock, nom_recherche)
        if suggestions:
            ifc.afficher_suggestions(suggestions, nom_recherche)
            continue

        ifc.afficher_produit_non_trouve(nom_recherche)


def _gerer_renommage(
    stock: list[types_structure.Produit]
) -> donnees.ResultatSauvegardeFichier:
    while True:
        ifc.afficher_entete_renommage()

        if not stock:
            ifc.afficher_renommage_impossible()
            return donnees.ResultatSauvegardeFichier.ANNULATION

        nom_produit = ifc.demander_nom_produit(LBL_NOM_PRODUIT)
        if nom_produit is None:
            return donnees.ResultatSauvegardeFichier.ANNULATION
        
        produit = gs.trouver_produit(stock, nom_produit)
        if produit is None:
            ifc.afficher_produit_non_trouve(nom_produit)
            continue

        while True:
            ancien_nom = produit[CLE_NOM]
            nouveau_nom = ifc.demander_nouveau_nom_produit(ancien_nom)
            if nouveau_nom is None:
                return donnees.ResultatSauvegardeFichier.ANNULATION
                
            if gs.verifier_nom_disponible(
                stock, produit[CLE_NOM], nouveau_nom
            ):
                gs.renommer_produit(produit, nouveau_nom)
                resultat_sauvegarde = donnees.sauvegarder_stock(stock)
                if resultat_sauvegarde is not donnees.ResultatSauvegardeFichier.SUCCES:
                    return resultat_sauvegarde

                ifc.afficher_produit_renomme(ancien_nom, nouveau_nom)
                break
                
            ifc.afficher_produit_existe(nouveau_nom)


def main():
    chargement_fichier, stock, anomalies_du_fichier = donnees.charger_stock()

    if chargement_fichier is donnees.ResultatChargementFichier.ACCES_FICHIER_REFUSE:
        ifc.afficher_erreur_fichier(chargement_fichier)
        return
    
    if chargement_fichier is not donnees.ResultatChargementFichier.SUCCES:
        ifc.afficher_erreur_fichier(chargement_fichier)
    
    if anomalies_du_fichier:
        ifc.afficher_anomalies_fichier(anomalies_du_fichier)

    continuer = True
    while continuer:
        ifc.effacer_ecran_terminal()
        choix_menu = ifc.afficher_et_demander_choix_menu()

        resultat_sauvegarde = donnees.ResultatSauvegardeFichier.ANNULATION

        ifc.effacer_ecran_terminal()
        match choix_menu.capitalize():
            case const.MENUP_CHOIX_STOCK:
                ifc.afficher_stock(stock)

            case const.MENUP_CHOIX_ALERTES:
                alertes = gs.trouver_alertes(stock)
                ifc.afficher_alertes(stock, alertes)

            case const.MENUP_CHOIX_AJOUT_MODIF:
                resultat_sauvegarde = _gerer_ajout_modification(stock)

            case const.MENUP_CHOIX_SUPPRESSION:
                resultat_sauvegarde = _gerer_suppression(stock)

            case const.MENUP_CHOIX_RECHERCHE:
                _gerer_recherche(stock)

            case const.MENUP_CHOIX_RENOMMAGE:
                resultat_sauvegarde = _gerer_renommage(stock)

            case const.MENUP_CHOIX_INVENTAIRE:
                ifc.afficher_inventaire(stock)

            case const.MENUP_CHOIX_QUITTER:
                continuer = False
        
        if resultat_sauvegarde is donnees.ResultatSauvegardeFichier.ACCES_FICHIER_REFUSE:
            continuer = False
            ifc.afficher_erreur_fichier(resultat_sauvegarde)


if __name__ == "__main__":
    main()