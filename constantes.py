#Fichiers du programme
FICHIER_STOCK = "stock.json"

#Clés du type Produit
CLE_NOM = "nom"
CLE_QUANTITE = "quantite"
CLE_SEUIL = "seuil"
CLE_PRIX = "prix"

#Retour des fonctions
RETOUR_AJOUT = 1
RETOUR_MODIFICATION = 2

#Gestion des erreurs
NO_ERR = 0
ERR_FILE_NOT_FOUND = 1
ERR_JSON_DECODE_ERROR = 2
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

#Aide à la navigation
NAV_MSG_TOUCHE_ENTREE_RETOUR_MENU = (
    "\n('Entrée' pour revenir au menu principal) "
)
NAV_MSG_VIDE_RETOUR_MENU = (
    "('Nom à vide + Entrée' pour revenir au menu principal)"
)
NAV_MSG_ENTREE_POUR_CONTINUER = "\n(Appuyer sur 'Entrée' pour continuer)"

#Messages de contrôle
CTRL_NB_POSITIF = "Veuillez entrer un nombre positif ou nul"
CTRL_NB_VALIDE = "Veuillez entrer un nombre valide"
CTRL_PRIX_VALIDE = "Veuillez entrer un prix valide"
CTRL_NOM_TROP_LONG = "\tLe nom du produit ne doit pas dépasser {0} caractères"
CTRL_NOM_DIFFERENT = "Le nouveau nom doit être différent de '{0}'\n"
CTRL_NOM_EXISTE_DEJA = "'{0}' existe déjà\n"
CTRL_REP_OUI_NON = "Veuillez répondre par 'o' ou 'n'"
CTRL_REP_OUI = "O"
CTRL_REP_NON = "N"

#Questions
QST_SUPPRESSION = "Suppression (o/n) ? "

#Menu principal et sous menus
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
TITRE_SMENU_AJOUT_MODIF = "--- AJOUTER / MODIFIER un produit ---"
TITRE_SMENU_SUPPRESSION = "--- SUPPRIMER UN PRODUIT ---"
TITRE_SMENU_RECHERCHE = "--- RECHERCHER UN PRODUIT ---"
TITRE_SMENU_RENOMMAGE = "--- RENOMMER UN PRODUIT ---"
TITRE_SMENU_INVENTAIRE = "--- INVENTAIRE AU "

#Affichage des tableaux
TIRET_CADRE = "-"
LARGEUR_CADRE = 55   
LARGEUR_CADRE_INVENTAIRE = 73
LARGEUR_COL = 15
COL_PRODUIT = "produit"
COL_QUANTITE = "quantité"
COL_SEUIL = "seuil"
COL_PRIX = "prix UHT"
COL_TOTAL = "total HT"

#Labels
LBL_NOM_PRODUIT = "Produit : "
LBL_QUANTITE_PRODUIT = "Quantité : "
LBL_SEUIL_PRODUIT = "Seuil : "
LBL_PRIX_PRODUIT = "Prix : "
LBL_NOUVEAU_NOM_PRODUIT = "Nouvelle appellation : "

#Affichage d'informations sur les produits
INFO_PRODUIT = "'{0}' : {1} (seuil: {2}) - prix UHT: {3:.2f} €"
INFO_COUT_STOCK = "Total du stock : {0:0.2f} €"
INFO_VALEUR_ACTU = "\tModification de "
INFO_PRODUIT_AJOUTE = "\tAjout de '{0}'"
INFO_STOCK_VIDE = (
    "Aucun produit enregistré.\nPour ajouter un produit aller dans "
    "le menu 'Ajouter / modifier un produit'."
)
INFO_PROD_AJOUTE = "Le produit a été ajouté"
INFO_PROD_MODIFIE = "Le produit a été modifié"
INFO_PROD_NON_TROUVE = "\nProduit introuvable"
INFO_PROD_SUPPRIME = "\nLe produit '{0}' a été supprimé"
INFO_AUCUNE_ALERTE = "\nStock OK, rien à recharger"
INFO_PROD_RENOMME = "\nLe produit '{0}' a été renommé en '{1}'"

#Gestion des anomalies dans le fichier de données
ANO_ENTIER = "int"
ANO_FLOTTANT = "float"
ANO_LISTE = (
    "\nATTENTION : des anomalies existent dans le fichier {0} :\n".format(
        FICHIER_STOCK
    )
)
ANO_MSG_NOUVEAU_FICHIER_STOCK = (
    "\nUn nouveau fichier '{0}' sera créé et remplacera l'existant à l'ajout, "
    "modification ou suppression d'un produit.".format(FICHIER_STOCK)
)
NO_ANO = "Produit OK"
ANO_NOM_INEXISTANTE = "Pas de champ '{0}', le produit sera ignoré".format(CLE_NOM)
ANO_CHAMP_PAS_STR = (
    "Le champ '{0}' n'est pas une chaîne de caractères, "
    "le produit sera ignoré"
)
ANO_CHAMP_TROP_LONG = "Le champ '{0}' dépasse {1} caractères, il sera tronqué"
ANO_CHAMP_VIDE = "Le champ '{0}' est vide"
ANO_NO_PRODUIT = "Produit n°{0} : "
ANO_CHAMP_NUM_CONV_ENTIER_OU_FLOTTANT = "Le champ '{0}' a été converti en '{1}'"
ANO_CHAMP_NUM_CONV_VAL = (
    "Le champ '{0}' a été converti en nombre avec la valeur '{1}'"
)
ANO_CHAMP_NUM_CONV_ZERO = (
    "Le champ '{0}' a été converti en nombre avec une valeur à 0"
)
ANO_CHAMP_NUM_INEXISTANT = (
    "Le champ '{0}' n'existe pas et a été créé avec une valeur à 0"
)