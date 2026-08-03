# Fichiers et dossiers du programme
FICHIER_STOCK = "stock.json"
FICHIER_STOCK_TEMP = "stock.tmp"
DOSSIER_ANOMALIES = "anomalies"
PREFIXE_DOSSIER_RAPPORT_ANOMALIES = "rapport-"
FICHIER_STOCK_ANO = FICHIER_STOCK + ".ano"
FICHIER_ANOMALIES = "anomalies.txt"
TXT_DATE_HEURE_RAPPORT_ANO = "Rapport créé le "
CARACTERE_SEPARATEUR = "="
TXT_SEPARATEUR = f"\n{CARACTERE_SEPARATEUR*60}\n"
TXT_PRODUIT_NO = "Produit n°"
TXT_PRODUIT_ORIGINE = "\nProduit d'origine :\n"
TXT_ANOMALIES = "\n\nAnomalies :"
TXT_RESULTAT = "\n\nRésultat :\n"
TXT_PRODUIT_NON_CONSERVE = "Ce produit n'a pas été conservé."

# Clés du type Produit
CLE_NOM = "nom"
CLE_QUANTITE = "quantite"
CLE_SEUIL = "seuil"
CLE_PRIX = "prix"

# Gestion des erreurs
ERR_MSG_FICHIER_MAUVAISE_STRUCTURE = (
    "\nLa structure du fichier de données '{0}' n'est pas adaptée.".format(
        FICHIER_STOCK
    )
)
ERR_MSG_FICHIER_STRUCTURE_LISTE_OBLIGATOIRE = (
    "Les données attendues doivent être une liste de produits."
)
ERR_MSG_FICHIER_STOCK_ABSENT = (
    "\nLe fichier stock.json n'existe pas. Il sera créé à l'ajout du "
    "premier produit."
)
ERR_MSG_FICHIER_STOCK_ENDOMMAGE = (
    "\nImpossible de lire le fichier '{0}' (fichier endommagé).".format(
        FICHIER_STOCK
    )
)
ERR_MSG_NOUVEAU_FICHIER_STOCK = (
    "Un nouveau fichier '{0}' sera créé et remplacera l'existant à "
    "l'ajout du premier produit.".format(
        FICHIER_STOCK
    )
)
ERR_MSG_SAUVER_FICHIER_STOCK_ENDOMMAGE = (
    "Si vous voulez garder votre fichier '{0}', sauvegardez-le "
    "ailleurs ou renommez-le avant de continuer.".format(FICHIER_STOCK)
)
ERR_MSG_PERMISSION_REFUSEE = (
    "Impossible d'accéder au fichier '{0}'. Vérifiez que vous disposez des droits "
    "nécessaires sur le fichier ou son dossier.".format(FICHIER_STOCK)
)
ERR_MSG_SAUVEGARDE_ECHOUEE = (
    "La sauvegarde du stock a échoué. La dernière modification n'a pas été prise en compte."
)
ERR_MSG_ERREUR_ECRITURE = (
    "Une erreur est survenue lors de l'écriture du fichier stock.json. Vérifiez que "
    "le support de stockage est accessible et qu'il dispose de suffisamment d'espace libre."
)
ERR_MSG_DONNEES_NON_SERIALISABLES = (
    "Une erreur interne est survenue lors de l'écriture du fichier stock.json. "
    "Les données ne peuvent pas être converties au format JSON."
)
ERR_MSG_ARRET_PROGRAMME = "Le programme va s'arrêter."

# Aide à la navigation
NAV_MSG_ENTREE_POUR_CONTINUER = "\n(Appuyer sur 'Entrée' pour continuer)"
NAV_RETOUR_MENU = "[Entrée] : retour au menu principal"
NAV_PAGE_PRECEDENTE = f"{'[p + Entrée] : précédente':26}"
NAV_PAGE_SUIVANTE = "[s + Entrée] : suivante"
NAV_PAGE_PRECEDENTE_VIDE = f"{' ':26}"
# Retours de navigation dans les pages d'un tableau
NAV_RETOUR_SEUL = 0
NAV_RETOUR_PRECEDENT = 1
NAV_RETOUR_SUIVANT = 2
NAV_RETOUR_PRECEDENT_SUIVANT = 3

# Messages de contrôle
CTRL_NB_POSITIF = "Veuillez entrer un nombre positif ou nul."
CTRL_NB_VALIDE = "Veuillez entrer un nombre valide."
CTRL_PRIX_VALIDE = "Veuillez entrer un prix valide."
CTRL_NOM_TROP_LONG = "\tLe nom du produit ne doit pas dépasser {0} caractères."
CTRL_NOM_EXISTE_DEJA = "'{0}' existe déjà.\n"
CTRL_REP_OUI_NON = "Veuillez répondre par 'o' ou 'n'."
CTRL_REP_OUI = "O"
CTRL_REP_NON = "N"
CTRL_CHOIX_ENTREE_OU_P = (
    "Choix invalide. Veuillez choisir entre 'Entrée' ou 'p + Entrée'."
)
CTRL_CHOIX_ENTREE_OU_S = (
    "Choix invalide. Veuillez choisir entre 'Entrée' ou 's + Entrée'."
)
CTRL_CHOIX_ENTREE_OU_P_OU_S = (
    "Choix invalide. Veuillez choisir entre 'Entrée', 'p + Entrée' ou 's + Entrée'."
)

# Questions
QST_SUPPRESSION = "Confirmer la suppression du produit '{0}' (o/n) ? "
QST_RETOUR_MENU_PRINCIPAL = (
    "Annuler la saisie en cours et revenir au menu principal (o/n) ? "
)

# Menu principal et sous menus
TITRE_MENU_PRINCIPAL = "--- MENU PRINCIPAL ---"
MENUP_SM_STOCK = "1. Afficher le stock"
MENUP_SM_ALERTES = "2. Voir les alertes"
MENUP_SM_AJOUT_MODIF = "3. Ajouter / modifier un produit"
MENUP_SM_SUPPRESSION = "4. Supprimer un produit"
MENUP_SM_RECHERCHE = "5. Rechercher un produit"
MENUP_SM_RENOMMAGE = "6. Renommer un produit"
MENUP_SM_INVENTAIRE = "7. Inventaire"
MENUP_SM_QUITTER = "Q. Quitter"
MENUP_CHOIX = "\nChoix : "
MENUP_REPETER_CHOIX = "Choix (1 à 7 ou Q) : "
LISTE_CHOIX = ["1", "2", "3", "4", "5", "6", "7", "Q", "q"]
MENUP_CHOIX_STOCK = "1"
MENUP_CHOIX_ALERTES = "2"
MENUP_CHOIX_AJOUT_MODIF = "3"
MENUP_CHOIX_SUPPRESSION = "4"
MENUP_CHOIX_RECHERCHE = "5"
MENUP_CHOIX_RENOMMAGE = "6"
MENUP_CHOIX_INVENTAIRE = "7"
MENUP_CHOIX_QUITTER = "Q"

TITRE_SMENU_STOCK = "--- ETAT DU STOCK ---"
TITRE_SMENU_ALERTES = "--- PRODUITS EN ALERTE ---"
TITRE_SMENU_AJOUT_MODIF = "--- AJOUTER / MODIFIER UN PRODUIT ---"
TITRE_SMENU_SUPPRESSION = "--- SUPPRIMER UN PRODUIT ---"
TITRE_SMENU_RECHERCHE = "--- RECHERCHER UN PRODUIT ---"
TITRE_SMENU_RENOMMAGE = "--- RENOMMER UN PRODUIT ---"
TITRE_SMENU_INVENTAIRE = "--- INVENTAIRE AU "

NB_LIGNES_VIDES_INTER_ACTION = 2

# Affichage des tableaux
TIRET_CADRE = "-"
LARGEUR_CADRE = 61
LARGEUR_CADRE_INVENTAIRE = 79
LARGEUR_COL = 15
LARGEUR_COL_NUMERO_LIGNE = 4
COL_NUMERO_LIGNE = "n°"
COL_PRODUIT = "produit"
COL_QUANTITE = "quantité"
COL_SEUIL = "seuil d'alerte"
COL_PRIX = "prix UHT"
COL_TOTAL = "total HT"
NB_PRODUITS_PAR_PAGE = 10
NUMEROTATION_PAGE = "Page {0}/{1}\n"
CHOIX_PAGE_SUIVANTE = "S"
CHOIX_PAGE_PRECEDENTE = "P"
CHOIX_RETOUR_MENU = ""
NB_LIGNES_VIDES_SOUS_TABLEAU = 3
TAILLE_MAX_NOM_PRODUIT = LARGEUR_COL

# Labels
LBL_NOM_PRODUIT = "Produit \t: "
LBL_QUANTITE_PRODUIT = "Quantité \t: "
LBL_SEUIL_PRODUIT = "Seuil d'alerte \t: "
LBL_PRIX_PRODUIT = "Prix \t\t: "
LBL_NOUVEAU_NOM_PRODUIT = "Nouvelle appellation de '{0}' : "

# Affichage d'informations sur les produits
INFO_PRODUIT = "'{0}' : {1} (seuil d'alerte : {2}) - prix UHT : {3} €"
INFO_COUT_STOCK = "Total du stock : {0:0.2f} €"
INFO_PRODUIT_MODIF_EN_COURS = "\tModification en cours de "
INFO_PRODUIT_AJOUT_EN_COURS = "\tAjout en cours de '{0}'"
INFO_STOCK_VIDE = (
    "Aucun produit enregistré.\nPour ajouter un produit aller dans "
    "le menu 'Ajouter / modifier un produit'."
)
INFO_PROD_AJOUTE = "Le produit '{0}' a été ajouté."
INFO_PROD_MODIFIE = "Le produit '{0}' a été modifié."
INFO_PROD_NON_TROUVE = "Le produit '{0}' est introuvable."
INFO_PROD_SUPPRIME = "Le produit '{0}' a été supprimé."
INFO_AUCUNE_ALERTE = "Stock OK, rien à recharger."
INFO_PROD_RENOMME = "\nLe produit '{0}' a été renommé en '{1}'."
INFO_RECHERCHE_STOCK_VIDE = "Le stock est vide : recherche impossible."
INFO_SUPPRESSION_STOCK_VIDE = "Le stock est vide : suppression impossible."
INFO_RENOMMAGE_STOCK_VIDE = "Le stock est vide : renommage impossible."


# Gestion des anomalies dans le fichier de données
ANO_ENTIER = "int"
ANO_FLOTTANT = "float"
ANO_LISTE = (
    "\nATTENTION : des anomalies existent dans le fichier '{0}'.\n".format(
        FICHIER_STOCK
    )
)
ANO_MSG_INFO_RAPPORT = (
    "Vous trouverez dans le dossier '{0}' une copie de ce fichier ainsi que son "
    "rapport d'anomalies."
)
ANO_MSG_ERR_CREATION_RAPPORT = (
    "Une erreur est survenue lors de la création du rapport d'anomalies. "
    "La sauvegarde de '{0}' et son rapport d'anomalies "
    "n'ont peut-être pas été effectués.".format(FICHIER_STOCK)
)
ANO_MSG_NOUVEAU_FICHIER_STOCK = (
    "\nUn nouveau fichier '{0}' remplacera l'existant lors de la prochaine "
    "modification du stock.".format(FICHIER_STOCK)
)
NO_ANO = "Produit OK"
ANO_NOM_INEXISTANT = "Pas de champ '{0}'.".format(CLE_NOM)
ANO_NOM_VIDE = "Le champ '{0}' est vide.".format(CLE_NOM)
ANO_NOM_DOUBLON = "Le produit '{0}' existe déjà dans le stock."
ANO_CHAMP_PAS_STR = (
    "Le champ '{0}' n'est pas une chaîne de caractères."
)
ANO_CHAMP_TROP_LONG = "Le champ '{0}' dépasse {1} caractères, il sera tronqué."
ANO_NO_PRODUIT = "Produit n°{0} : "
ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT = (
    "Le champ '{0}' a été converti en '{1}', sa valeur peut être tronquée."
)
ANO_CHAMP_NUM_CONV_VAL = (
    "Le champ '{0}' a été converti en nombre avec la valeur '{1}'."
)
ANO_CHAMP_NUM_CONV_ZERO = (
    "Le champ '{0}' a été converti en nombre avec une valeur à 0."
)
ANO_CHAMP_NUM_INEXISTANT = (
    "Le champ '{0}' n'existe pas et a été créé avec une valeur à 0."
)
ANO_PRODUIT_STRUCTURE_INVALIDE = (
    "La structure du produit n'est pas valide "
    "(structure attendue : un dictionnaire)."
)
ANO_CHAMP_INVALIDE = (
    "Le champ '{0}' n'est pas valide, il ne sera pas conservé."
)
ANO_ARRET_VERIFICATION = (
    "La vérification du produit a été interrompue "
    "après la détection d'une anomalie bloquante."
)

# Suggestions de recherche
RECH_NB_ELEMENTS_RETOUR = 5
RECH_SEUIL_SIMILARITE = 0.5 # de 0.0 (très permissif) à 1.0 (strictement identique)
RECH_SUGGESTIONS = "Suggestions possibles :"
RECH_NOM_SUGGERE = "- {0}"

# Formatage de texte
FORMAT_RESET = "\033[0m"
FORMAT_ROUGE = "\033[31m"