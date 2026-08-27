from normalisation import normaliser_chaine_pour_comparaison


def test_normaliser_chaine_pour_comparaison():
    chaine_entree = "Café"
    chaine_attendue = "cafe"

    chaine_sortie = normaliser_chaine_pour_comparaison(chaine_entree)

    assert chaine_sortie == chaine_attendue