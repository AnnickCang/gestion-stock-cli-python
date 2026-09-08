import pytest

from normalisation import normaliser_chaine_pour_comparaison


@pytest.mark.parametrize(
    ("chaine_entree", "chaine_attendue"),
    [
        ("Café", "cafe"),
        ("caramel", "caramel"),
        ("décaféiné", "decafeine"),
        ("ÀÂÉÈÊÙÛÔÎ", "aaeeeuuoi"),
        ("m&ms", "m&ms"),
        ("Niño", "nino"),
        ("<>*/- @&", "<>*/- @&"),
        ("", ""),
    ],
)


def test_normaliser_chaine_pour_comparaison(chaine_entree, chaine_attendue):
    chaine_sortie = normaliser_chaine_pour_comparaison(chaine_entree)

    assert chaine_sortie == chaine_attendue