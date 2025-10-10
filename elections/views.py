from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F, Q
from .models import Candidat, CentreVote, BureauVote, Resultat


def resultats_globaux(request):
    """Vue principale des résultats globaux"""
    candidats = Candidat.objects.all()

    # Calculer les statistiques globales
    total_voix = Resultat.objects.aggregate(
        total=Sum('nombre_voix')
    )['total'] or 0

    total_inscrits = BureauVote.objects.aggregate(
        total=Sum('nombre_inscrits')
    )['total'] or 0

    taux_participation = 0
    if total_inscrits > 0:
        taux_participation = round((total_voix / total_inscrits) * 100, 2)

    # Préparer les données des candidats
    resultats_candidats = []
    for candidat in candidats:
        voix = candidat.total_voix()
        pourcentage = candidat.pourcentage_global()
        resultats_candidats.append({
            'candidat': candidat,
            'voix': voix,
            'pourcentage': pourcentage
        })

    # Trier par nombre de voix décroissant
    resultats_candidats.sort(key=lambda x: x['voix'], reverse=True)

    context = {
        'resultats_candidats': resultats_candidats,
        'total_voix': total_voix,
        'total_inscrits': total_inscrits,
        'taux_participation': taux_participation,
    }

    return render(request, 'elections/resultats_globaux.html', context)


def resultats_par_centre(request):
    """Résultats détaillés par centre de vote"""
    centres = CentreVote.objects.all().prefetch_related('bureaux__resultats__candidat')

    centres_data = []
    for centre in centres:
        # Résultats par candidat pour ce centre
        resultats_centre = []
        candidats = Candidat.objects.all()
        total_voix_centre = centre.total_voix()

        for candidat in candidats:
            voix = Resultat.objects.filter(
                candidat=candidat,
                bureau_vote__centre=centre
            ).aggregate(total=Sum('nombre_voix'))['total'] or 0

            pourcentage = 0
            if total_voix_centre > 0:
                pourcentage = round((voix / total_voix_centre) * 100, 2)

            resultats_centre.append({
                'candidat': candidat,
                'voix': voix,
                'pourcentage': pourcentage
            })

        resultats_centre.sort(key=lambda x: x['voix'], reverse=True)

        centres_data.append({
            'centre': centre,
            'resultats': resultats_centre,
            'total_voix': total_voix_centre,
            'total_inscrits': centre.total_inscrits()
        })

    context = {
        'centres_data': centres_data
    }

    return render(request, 'elections/resultats_par_centre.html', context)


def resultats_par_bureau(request):
    """Résultats détaillés de tous les bureaux de vote"""
    bureaux = BureauVote.objects.all().select_related('centre').prefetch_related('resultats__candidat')
    candidats = Candidat.objects.all().order_by('numero')

    bureaux_data = []
    for bureau in bureaux:
        resultats_bureau = []
        total_voix_bureau = bureau.total_voix()

        for candidat in candidats:
            try:
                resultat = Resultat.objects.get(candidat=candidat, bureau_vote=bureau)
                voix = resultat.nombre_voix
            except Resultat.DoesNotExist:
                voix = 0

            pourcentage = 0
            if total_voix_bureau > 0:
                pourcentage = round((voix / total_voix_bureau) * 100, 2)

            resultats_bureau.append({
                'candidat': candidat,
                'voix': voix,
                'pourcentage': pourcentage
            })

        # Trouver le gagnant
        gagnant = max(resultats_bureau, key=lambda x: x['voix']) if resultats_bureau else None

        bureaux_data.append({
            'bureau': bureau,
            'resultats': resultats_bureau,
            'total_voix': total_voix_bureau,
            'taux_participation': bureau.taux_participation(),
            'gagnant': gagnant
        })

    context = {
        'bureaux_data': bureaux_data,
        'candidats': candidats
    }

    return render(request, 'elections/resultats_par_bureau.html', context)


def detail_bureau(request, bureau_id):
    """Détails d'un bureau de vote spécifique"""
    bureau = get_object_or_404(BureauVote, id=bureau_id)
    resultats = Resultat.objects.filter(bureau_vote=bureau).select_related('candidat')

    total_voix = bureau.total_voix()

    resultats_data = []
    for resultat in resultats:
        pourcentage = 0
        if total_voix > 0:
            pourcentage = round((resultat.nombre_voix / total_voix) * 100, 2)

        resultats_data.append({
            'candidat': resultat.candidat,
            'voix': resultat.nombre_voix,
            'pourcentage': pourcentage
        })

    resultats_data.sort(key=lambda x: x['voix'], reverse=True)

    context = {
        'bureau': bureau,
        'resultats': resultats_data,
        'total_voix': total_voix,
        'taux_participation': bureau.taux_participation()
    }

    return render(request, 'elections/detail_bureau.html', context)

