import os
from datetime import datetime

import types_structure
import constantes as const
from gestion_stock import verifier_quantite_sous_seuil
from gestion_stock import verifier_prix_nul
from donnees import ResultatChargementFichier
from donnees import ResultatSauvegardeFichier


CLE_NOM = const.CLE_NOM
CLE_QUANTITE = const.CLE_QUANTITE
CLE_SEUIL = const.CLE_SEUIL
CLE_PRIX = const.CLE_PRIX
LARGEUR_COL = const.LARGEUR_COL
LARGEUR_CADRE = const.LARGEUR_CADRE
LARGEUR_CADRE_INVENTAIRE = const.LARGEUR_CADRE_INVENTAIRE
TIRET_CADRE = const.TIRET_CADRE
NB_PRODUITS_PAR_PAGE = const.NB_PRODUITS_PAR_PAGE
NB_LIGNES_VIDES_SOUS_TABLEAU = const.NB_LIGNES_VIDES_SOUS_TABLEAU
NB_LIGNES_VIDES_INTER_ACTION = const.NB_LIGNES_VIDES_INTER_ACTION


def _afficher_lignes_vides(nb_lignes: int = 1) -> None:
    for _ in range(nb_lignes):
        print()


def _afficher_bordure_horizontale(largeur_cadre: int) -> None:
    print(TIRET_CADRE * largeur_cadre)


def _afficher_stock_vide() -> None:
    print(const.INFO_STOCK_VIDE)


def _attendre_touche_entree() -> None:
    _afficher_lignes_vides()
    input()


def _attendre_touche_entree_avec_message() -> None:
    input(const.NAV_MSG_ENTREE_POUR_CONTINUER)


def _attendre_touche_entree_pour_retour_menu() -> None:
    _afficher_lignes_vides()
    input(const.NAV_RETOUR_MENU)


def _attendre_choix_navigation_page(choix_possible: int) -> str:
    """Renvoie un choix valide pour naviguer dans les pages d'un affichage
    ou revenir au menu principal"""
    MENUP_CHOIX = const.MENUP_CHOIX
    RETOUR_MENU = const.CHOIX_RETOUR_MENU
    PAGE_PRECEDENTE = const.CHOIX_PAGE_PRECEDENTE
    PAGE_SUIVANTE = const.CHOIX_PAGE_SUIVANTE

    if choix_possible == const.NAV_RETOUR_SEUL:
        input()
        return RETOUR_MENU
    
    choix = input(MENUP_CHOIX).strip().upper()
    match choix_possible:
        case const.NAV_RETOUR_PRECEDENT:
            while choix not in [RETOUR_MENU, PAGE_PRECEDENTE]:
                print(const.CTRL_CHOIX_ENTREE_OU_P)
                choix = input(MENUP_CHOIX).strip().upper()
        case const.NAV_RETOUR_SUIVANT:
            while choix not in [RETOUR_MENU, PAGE_SUIVANTE]:
                print(const.CTRL_CHOIX_ENTREE_OU_S)
                choix = input(MENUP_CHOIX).strip().upper()
        case const.NAV_RETOUR_PRECEDENT_SUIVANT:
            while choix not in [RETOUR_MENU, PAGE_PRECEDENTE, PAGE_SUIVANTE]:
                print(const.CTRL_CHOIX_ENTREE_OU_P_OU_S)
                choix = input(MENUP_CHOIX).strip().upper()
    return choix


def _afficher_nom_colonnes_stock_et_alertes() -> None:
    _afficher_bordure_horizontale(LARGEUR_CADRE)
    print(f"| {const.COL_NUMERO_LIGNE:>{const.LARGEUR_COL_NUMERO_LIGNE}} "
          f"| {const.COL_PRODUIT:{LARGEUR_COL}} "
          f"| {const.COL_QUANTITE:>{LARGEUR_COL}} "
          f"| {const.COL_SEUIL:>{LARGEUR_COL}} |"
    )
    _afficher_bordure_horizontale(LARGEUR_CADRE)


def _afficher_nom_colonnes_inventaire() -> None:
    _afficher_bordure_horizontale(LARGEUR_CADRE_INVENTAIRE)
    print(f"| {const.COL_NUMERO_LIGNE:>{const.LARGEUR_COL_NUMERO_LIGNE}} "
          f"| {const.COL_PRODUIT:{LARGEUR_COL}} "
          f"| {const.COL_QUANTITE:>{LARGEUR_COL}} "
          f"| {const.COL_PRIX:>{LARGEUR_COL}} "
          f"| {const.COL_TOTAL:>{LARGEUR_COL}} |"
    )
    _afficher_bordure_horizontale(LARGEUR_CADRE_INVENTAIRE)


def _demander_retour_menu() -> bool:
    while True:
        entree_utilisateur = input(const.QST_RETOUR_MENU_PRINCIPAL).strip()
        match entree_utilisateur.capitalize():
            case const.CTRL_REP_OUI:
                return True
            case const.CTRL_REP_NON:
                return False
        print(const.CTRL_REP_OUI_NON)


def _demander_entier_positif(message: str) -> int | None:
    """Renvoie l'entrée utilisateur après l'avoir convertie en entier
    ou None (si champ vide avec validation retour au menu principal)"""
    while True:
        entree_utilisateur = input(message).strip()
        if not entree_utilisateur: 
            if _demander_retour_menu():
                return None
            continue

        try:
            valeur = int(entree_utilisateur)
            if valeur >= 0:
                return valeur
            print(const.CTRL_NB_POSITIF)
        except ValueError:
            print(const.CTRL_NB_VALIDE)


def _demander_flottant_positif(message: str) -> float | None:
    """Renvoie l'entrée utilisateur après l'avoir convertie en float
    ou None (si champ vide avec validation retour au menu principal)"""
    while True:
        entree_utilisateur = input(message).strip()
        if not entree_utilisateur:
            if _demander_retour_menu():
                return None
            continue

        try:
            valeur = float(entree_utilisateur)
            if valeur >= 0:
                return valeur
            print(const.CTRL_PRIX_VALIDE)
        except ValueError:
            print(const.CTRL_NB_VALIDE)


def _afficher_titre_de_sous_menu(titre: str, largeur_cadre: int) -> None:
    print(f"{titre:^{largeur_cadre}}")


def _afficher_entree_pour_retour_menu(largeur_cadre: int) -> None:
    nav_retour_menu = f"( {const.NAV_RETOUR_MENU} )"
    print(f"{nav_retour_menu:^{largeur_cadre}}")
    _afficher_lignes_vides()


def _afficher_aide_navigation_page(page_courante: int, total_pages: int) -> int:
    RETOUR_MENU = const.NAV_RETOUR_MENU
    page_precedente = const.NAV_PAGE_PRECEDENTE
    page_suivante = const.NAV_PAGE_SUIVANTE
    page_precedente_vide = const.NAV_PAGE_PRECEDENTE_VIDE

    if (page_courante == 1) and (page_courante == total_pages):
        print(f"{RETOUR_MENU}")
        return const.NAV_RETOUR_SEUL

    if page_courante == 1:
        print(f"{RETOUR_MENU} - {page_precedente_vide} - {page_suivante}")
        return const.NAV_RETOUR_SUIVANT
    
    if page_courante == total_pages:
        print(f"{RETOUR_MENU} - {page_precedente} -")
        return const.NAV_RETOUR_PRECEDENT
    
    print(f"{RETOUR_MENU} - {page_precedente} - {page_suivante}")
    return const.NAV_RETOUR_PRECEDENT_SUIVANT


def _calculer_total_pages(produits: list[types_structure.Produit]) -> int:
    """Renvoie le nombre total de pages pour une liste de produits à afficher
    avec n produits par page"""
    nb_produits = len(produits)
    total_pages = nb_produits // NB_PRODUITS_PAR_PAGE
    if (nb_produits % NB_PRODUITS_PAR_PAGE != 0):
        total_pages +=1
    return total_pages


def _mettre_a_jour_page_courante(
    choix_navigation: int,
    page_courante: int
) -> int | None:
    """Renvoie le numéro de la page courante après le choix de navigation"""
    match _attendre_choix_navigation_page(choix_navigation):
        case const.CHOIX_PAGE_PRECEDENTE:
            return page_courante - 1
        case const.CHOIX_PAGE_SUIVANTE:
            return page_courante + 1
        case const.CHOIX_RETOUR_MENU:
            return None


def _completer_sous_tableau_avec_lignes_vides(
    condition: bool,
    nb_lignes_vides: int
) -> None:
    if condition:
        _afficher_lignes_vides(nb_lignes_vides)


def _formater_texte_en_rouge(texte: str, condition: bool) -> str:
    if condition:
        return f"{const.FORMAT_ROUGE}{texte}{const.FORMAT_RESET}"
    return texte


def _formater_info_produit(
    produit: types_structure.Produit
) -> types_structure.InfosProduitFormatees:
    nom = produit[CLE_NOM]
    quantite = _formater_texte_en_rouge(
        str(produit[CLE_QUANTITE]),
        verifier_quantite_sous_seuil(produit)
    )
    seuil = str(produit[CLE_SEUIL])
    prix = f"{produit[CLE_PRIX]:.2f}"
    prix = _formater_texte_en_rouge(prix, verifier_prix_nul(produit))

    return types_structure.InfosProduitFormatees(nom, quantite, seuil, prix)


def effacer_ecran_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def demander_info_produit(
    produit: types_structure.Produit | None,
    nom_produit: str = ""
) -> types_structure.ChampsNumeriquesProduit | None:
    """Renvoie un dict ChampsNumeriquesProduit (saisies par l'utilisateur)
    ou None si la saisie est annulée"""
    if produit is None:
        print(const.INFO_PRODUIT_AJOUT_EN_COURS.format(nom_produit))
    else:
        nom, quantite, seuil, prix = _formater_info_produit(produit)
        infos_produit = const.INFO_PRODUIT.format(nom, quantite, seuil, prix)
        print(const.INFO_PRODUIT_MODIF_EN_COURS, infos_produit, sep='')

    quantite = _demander_entier_positif(const.LBL_QUANTITE_PRODUIT)
    if quantite is None:
        return None
    
    seuil = _demander_entier_positif(const.LBL_SEUIL_PRODUIT)
    if seuil is None:
        return None
    
    prix = _demander_flottant_positif(const.LBL_PRIX_PRODUIT)
    if prix is None:
        return None
    
    return {
        CLE_QUANTITE: quantite, 
        CLE_SEUIL: seuil, 
        CLE_PRIX: prix
    }


def demander_nom_produit(message: str) -> str | None:
    """Demande et renvoie un nom de produit ne dépassant pas une taille max
    ou None si la saisie est vide"""
    while True:
        nom: str = input(message).strip()
        if not nom:
            return None
        
        if len(nom) > const.TAILLE_MAX_NOM_PRODUIT:
            print(const.CTRL_NOM_TROP_LONG.format(const.TAILLE_MAX_NOM_PRODUIT))
            continue
        
        return nom


def demander_nouveau_nom_produit(ancien_nom: str) -> str | None:
    nouveau_nom = demander_nom_produit(
        const.LBL_NOUVEAU_NOM_PRODUIT.format(ancien_nom)
    )
    if nouveau_nom is None:
        return None
    
    return nouveau_nom


def demander_confirmation_suppression(nom_produit: str) -> bool:
    while True:
        _afficher_lignes_vides()
        question = const.QST_SUPPRESSION.format(nom_produit)
        entree_utilisateur = input(question).strip()
        match entree_utilisateur.capitalize():
            case const.CTRL_REP_OUI:
                return True
            case const.CTRL_REP_NON:
                _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)
                return False
        _afficher_lignes_vides()
        print(const.CTRL_REP_OUI_NON)


def afficher_stock(stock: list[types_structure.Produit]) -> None:
    """Affiche le stock actuel avec quantités et seuils et une pagination"""
    titre = const.TITRE_SMENU_STOCK
    
    if not stock:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
        _afficher_lignes_vides()
        _afficher_stock_vide()
        _attendre_touche_entree_pour_retour_menu()
        return
    
    debut = 0
    fin = NB_PRODUITS_PAR_PAGE
    page_courante = 1
    total_pages = _calculer_total_pages(stock)

    while True:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
        _afficher_lignes_vides()

        _afficher_nom_colonnes_stock_et_alertes()
        for numero, produit in enumerate(stock[debut:fin], start=1):
            no_ligne = f"{numero:>{const.LARGEUR_COL_NUMERO_LIGNE}}"
            nom = f"{produit[CLE_NOM]:{LARGEUR_COL}}"
            quantite = f"{produit[CLE_QUANTITE]:>{LARGEUR_COL}}"
            quantite = _formater_texte_en_rouge(
                quantite,
                verifier_quantite_sous_seuil(produit)
            )
            seuil = f"{produit[CLE_SEUIL]:>{LARGEUR_COL}}"
            print(f"| {no_ligne} | {nom} | {quantite} | {seuil} |")
        _afficher_bordure_horizontale(LARGEUR_CADRE)

        _completer_sous_tableau_avec_lignes_vides(
            page_courante == total_pages,
            NB_PRODUITS_PAR_PAGE - int(no_ligne)
        )

        _afficher_lignes_vides(NB_LIGNES_VIDES_SOUS_TABLEAU)
        print(const.NUMEROTATION_PAGE.format(page_courante, total_pages))

        choix_navigation = _afficher_aide_navigation_page(page_courante, total_pages)
        print(const.NAV_GENERER_FICHIER_IMPRIMABLE)
        page_courante = _mettre_a_jour_page_courante(choix_navigation, page_courante)
        if page_courante is None:
            break

        debut = (page_courante - 1) * NB_PRODUITS_PAR_PAGE
        fin = debut + NB_PRODUITS_PAR_PAGE

        effacer_ecran_terminal()


def afficher_alertes(
    stock: list[types_structure.Produit],
    alertes: list[types_structure.Produit]
) -> None:
    """Affiche la liste des noms de produits en dessous du seuil
    avec une pagination"""
    titre = const.TITRE_SMENU_ALERTES
    
    if not stock:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
        _afficher_lignes_vides()
        _afficher_stock_vide()
        _attendre_touche_entree_pour_retour_menu()
        return
    
    if not alertes:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
        _afficher_lignes_vides()
        print(const.INFO_AUCUNE_ALERTE)
        _attendre_touche_entree_pour_retour_menu()
        return
    
    debut = 0
    fin = NB_PRODUITS_PAR_PAGE
    page_courante = 1
    total_pages = _calculer_total_pages(alertes)

    while True:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
        _afficher_lignes_vides()

        _afficher_nom_colonnes_stock_et_alertes()
        for no_ligne, produit in enumerate(alertes[debut:fin], start=1):
            print(f"| {no_ligne:>{const.LARGEUR_COL_NUMERO_LIGNE}} "
                f"| {produit[CLE_NOM]:{LARGEUR_COL}} "
                f"| {produit[CLE_QUANTITE]:>{LARGEUR_COL}} "
                f"| {produit[CLE_SEUIL]:>{LARGEUR_COL}} |"
            )
        _afficher_bordure_horizontale(LARGEUR_CADRE)

        _completer_sous_tableau_avec_lignes_vides(
            page_courante == total_pages,
            NB_PRODUITS_PAR_PAGE - int(no_ligne)
        )

        _afficher_lignes_vides(NB_LIGNES_VIDES_SOUS_TABLEAU)
        print(const.NUMEROTATION_PAGE.format(page_courante, total_pages))

        choix_navigation = _afficher_aide_navigation_page(page_courante, total_pages)
        print(const.NAV_GENERER_FICHIER_IMPRIMABLE)
        page_courante = _mettre_a_jour_page_courante(choix_navigation, page_courante)
        if page_courante is None:
            break
        
        debut = (page_courante - 1) * NB_PRODUITS_PAR_PAGE
        fin = debut + NB_PRODUITS_PAR_PAGE

        effacer_ecran_terminal()


def afficher_info_produit(produit: types_structure.Produit) -> None:
    """Affiche les données relatives au produit recherché s'il a été trouvé"""
    nom, quantite, seuil, prix = _formater_info_produit(produit)
    _afficher_lignes_vides()
    print(f"{const.LBL_NOM_PRODUIT}{nom}")
    print(f"{const.LBL_QUANTITE_PRODUIT}{quantite}")
    print(f"{const.LBL_SEUIL_PRODUIT}{seuil}")
    print(f"{const.LBL_PRIX_PRODUIT}{prix}")
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)
        

def afficher_inventaire(stock: list[types_structure.Produit]) -> None:
    """Affiche les données d'inventaire avec une pagination.
    Le coût total du stock est affiché sur la dernière page."""
    jour = datetime.today().strftime("%d/%m/%Y")
    titre = const.TITRE_SMENU_INVENTAIRE + jour + " ---"
    
    if not stock:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE_INVENTAIRE)
        _afficher_lignes_vides()
        _afficher_stock_vide()
        _attendre_touche_entree_pour_retour_menu()
        return
    
    cout_total_stock = sum(
        produit[CLE_QUANTITE] * produit[CLE_PRIX]
        for produit in stock
    )

    debut = 0
    fin = NB_PRODUITS_PAR_PAGE
    page_courante = 1
    total_pages = _calculer_total_pages(stock)

    while True:
        _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE_INVENTAIRE)
        _afficher_lignes_vides()

        _afficher_nom_colonnes_inventaire()
        for numero, produit in enumerate(stock[debut:fin], start=1):
            no_ligne = f"{numero:>{const.LARGEUR_COL_NUMERO_LIGNE}}"
            cout_total_produit = produit[CLE_QUANTITE] * produit[CLE_PRIX]
            nom = f"{produit[CLE_NOM]:{LARGEUR_COL}}"
            quantite = f"{produit[CLE_QUANTITE]:>{LARGEUR_COL}}"
            prix = f"{produit[CLE_PRIX]:>{LARGEUR_COL}.2f}"
            prix = _formater_texte_en_rouge(
                prix,
                verifier_prix_nul(produit)
            )
            cout_total = f"{cout_total_produit:>{LARGEUR_COL}.2f}"
            print(f"| {no_ligne} | {nom} | {quantite} | {prix} | {cout_total} |")
        _afficher_bordure_horizontale(LARGEUR_CADRE_INVENTAIRE)

        if page_courante == total_pages:
            _completer_sous_tableau_avec_lignes_vides(
                True,
                NB_PRODUITS_PAR_PAGE - int(no_ligne)
            )
            texte_total_stock = const.INFO_COUT_STOCK.format(cout_total_stock)
            print(f"\n{texte_total_stock:>{LARGEUR_CADRE_INVENTAIRE}}\n")
        else:
            _afficher_lignes_vides(NB_LIGNES_VIDES_SOUS_TABLEAU)

        print(const.NUMEROTATION_PAGE.format(page_courante, total_pages))

        choix_navigation = _afficher_aide_navigation_page(page_courante, total_pages)
        print(const.NAV_GENERER_FICHIER_IMPRIMABLE)
        page_courante = _mettre_a_jour_page_courante(choix_navigation, page_courante)
        if page_courante is None:
            break

        debut = (page_courante - 1) * NB_PRODUITS_PAR_PAGE
        fin = debut + NB_PRODUITS_PAR_PAGE

        effacer_ecran_terminal()


def afficher_erreur_fichier(
    code_err: ResultatChargementFichier | ResultatSauvegardeFichier
) -> None:
    match code_err:
        case ResultatChargementFichier.FICHIER_INTROUVABLE:
            print(const.ERR_MSG_FICHIER_STOCK_ABSENT)
        case ResultatChargementFichier.JSON_INVALIDE:
            print(const.ERR_MSG_FICHIER_STOCK_ENDOMMAGE)
            print(const.ERR_MSG_NOUVEAU_FICHIER_STOCK)
            print(const.ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE)
        case ResultatChargementFichier.STOCK_PAS_UNE_LISTE:
            print(const.ERR_MSG_FICHIER_MAUVAISE_STRUCTURE)
            print(const.ERR_MSG_FICHIER_STRUCTURE_LISTE_OBLIGATOIRE)
            print(const.ERR_MSG_NOUVEAU_FICHIER_STOCK)
            print(const.ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE)
        case ResultatChargementFichier.ACCES_FICHIER_REFUSE:
            print(const.ERR_MSG_PERMISSION_REFUSEE)
            print(const.ERR_MSG_ARRET_PROGRAMME)
        case ResultatSauvegardeFichier.ACCES_FICHIER_REFUSE:
            _afficher_lignes_vides()
            print(const.ERR_MSG_SAUVEGARDE_ECHOUEE)
            print(const.ERR_MSG_PERMISSION_REFUSEE)
        case ResultatSauvegardeFichier.ERREUR_ECRITURE:
            _afficher_lignes_vides()
            print(const.ERR_MSG_SAUVEGARDE_ECHOUEE)
            print(const.ERR_MSG_ERREUR_ECRITURE)
        case ResultatSauvegardeFichier.DONNEES_NON_SERIALISABLES:
            _afficher_lignes_vides()
            print(const.ERR_MSG_SAUVEGARDE_ECHOUEE)
            print(const.ERR_MSG_DONNEES_NON_SERIALISABLES)
    _attendre_touche_entree_avec_message()


def afficher_anomalies_fichier(
    nom_dossier_anomalies: str | None
) -> None:
    print(const.ANO_LISTE)
    if nom_dossier_anomalies is None:
        print(const.ANO_MSG_ERR_CREATION_RAPPORT)
    else:
        print(const.ANO_MSG_INFO_RAPPORT.format(nom_dossier_anomalies))
    print(const.ANO_MSG_NOUVEAU_FICHIER_STOCK)
    _attendre_touche_entree_avec_message()


def afficher_et_demander_choix_menu() -> str:
    """Affiche le menu principal et renvoie le choix de l'utilisateur"""

    print(f"{const.TITRE_MENU_PRINCIPAL:^{LARGEUR_CADRE}}")
    _afficher_lignes_vides()
    print(const.MENUP_SM_STOCK)
    print(const.MENUP_SM_ALERTES)
    print(const.MENUP_SM_AJOUT_MODIF)
    print(const.MENUP_SM_SUPPRESSION)
    print(const.MENUP_SM_RECHERCHE)
    print(const.MENUP_SM_RENOMMAGE)
    print(const.MENUP_SM_INVENTAIRE)
    print(const.MENUP_SM_QUITTER)

    choix = input(const.MENUP_CHOIX).strip()
    while choix not in const.LISTE_CHOIX:
        choix = input(const.MENUP_REPETER_CHOIX).strip()
    
    return choix


def afficher_produit_ajoute(nom_produit: str) -> None:
    print(const.INFO_PROD_AJOUTE.format(nom_produit))
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)


def afficher_produit_modifie(nom_produit: str) -> None:
    print(const.INFO_PROD_MODIFIE.format(nom_produit))
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)


def afficher_produit_non_trouve(nom_produit: str) -> None:
    _afficher_lignes_vides()
    print(const.INFO_PROD_NON_TROUVE.format(nom_produit))
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)


def afficher_produit_supprime(nom_produit: str) -> None:
    print(const.INFO_PROD_SUPPRIME.format(nom_produit))
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)


def afficher_produit_renomme(ancien_nom: str, nouveau_nom: str) -> None:
    print(const.INFO_PROD_RENOMME.format(ancien_nom, nouveau_nom))
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)


def afficher_produit_existe(nom: str) -> None:
    print(const.CTRL_NOM_EXISTE_DEJA.format(nom))


def afficher_suggestions(suggestions: list[str], nom_produit: str) -> None:
    """Affiche une liste de suggestions pour la recherche d'un produit"""
    suggestions_pour_produit_non_trouve = (
        f"{const.INFO_PROD_NON_TROUVE.format(nom_produit)} "
        f"{const.RECH_SUGGESTIONS}"
    )
    print(suggestions_pour_produit_non_trouve)
    for suggestion in suggestions:
        print(const.RECH_NOM_SUGGERE.format(suggestion))
    _afficher_lignes_vides(NB_LIGNES_VIDES_INTER_ACTION)


def afficher_recherche_impossible() -> None:
    print(const.INFO_RECHERCHE_STOCK_VIDE)
    _attendre_touche_entree()


def afficher_suppression_impossible() -> None:
    print(const.INFO_SUPPRESSION_STOCK_VIDE)
    _attendre_touche_entree()


def afficher_renommage_impossible() -> None:
    print(const.INFO_RENOMMAGE_STOCK_VIDE)
    _attendre_touche_entree()


def afficher_entete_suppression() -> None:
    titre = const.TITRE_SMENU_SUPPRESSION
    _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
    _afficher_entree_pour_retour_menu(LARGEUR_CADRE)


def afficher_entete_recherche() -> None:
    titre = const.TITRE_SMENU_RECHERCHE
    _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
    _afficher_entree_pour_retour_menu(LARGEUR_CADRE)


def afficher_entete_renommage() -> None:
    titre = const.TITRE_SMENU_RENOMMAGE
    _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
    _afficher_entree_pour_retour_menu(LARGEUR_CADRE)


def afficher_entete_ajout_modification() -> None:
    titre = const.TITRE_SMENU_AJOUT_MODIF
    _afficher_titre_de_sous_menu(titre, LARGEUR_CADRE)
    _afficher_entree_pour_retour_menu(LARGEUR_CADRE)