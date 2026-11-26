"""Calcul des heures a partir des poincons (journal d'evenements de pointage).

Le totalisateur derive les heures travaillees des poincons : il appaire
chaque 'entree' avec la 'sortie' suivante et somme les durees.
"""

from datetime import timedelta


def calculer_total_heures(poincons):
    """Somme des durees (sortie - entree) en timedelta.

    Apparie chaque 'entree' avec la 'sortie' suivante ; ignore une
    'entree' sans 'sortie' (poincon en cours, jour pas encore termine).
    """
    total = timedelta()
    entree_en_cours = None
    for p in sorted(poincons, key=lambda x: x.horodatage):
        if p.type_poincon == "entree":
            entree_en_cours = p.horodatage
        elif p.type_poincon == "sortie" and entree_en_cours is not None:
            total += p.horodatage - entree_en_cours
            entree_en_cours = None
    return total


def regrouper_par_jour(poincons):
    """Retourne une liste de dicts {'jour', 'poincons', 'total'} tries par jour."""
    from collections import defaultdict

    par_jour = defaultdict(list)
    for p in poincons:
        par_jour[p.horodatage.date()].append(p)
    return [
        {"jour": jour, "poincons": items, "total": calculer_total_heures(items)}
        for jour, items in sorted(par_jour.items())
    ]
