from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Prefetch
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidat, CentreVote, BureauVote, Resultat
from .forms import BureauSelectForm, ResultatForm, CandidatForm, CentreVoteForm, BureauVoteForm

def dashboard(request):
    """Tableau de bord pour les agents (non-admin)"""
    return render(request, 'elections/dashboard.html')


def saisie_donnees(request):
    """Interface de saisie des résultats pour le staff"""
    bureau_id = request.GET.get('bureau')
    
    if not bureau_id:
        # Étape 1 : Choix du bureau
        form = BureauSelectForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            return redirect(f"{request.path}?bureau={form.cleaned_data['bureau'].id}")
            
        return render(request, 'elections/saisie_bureau.html', {'form': form})
        
    else:
        # Étape 2 : Saisie des résultats
        bureau = get_object_or_404(BureauVote, id=bureau_id)
        candidats = Candidat.objects.all().order_by('numero')
        
        if request.method == 'POST':
            saved_count = 0
            for candidat in candidats:
                voix = request.POST.get(f'candidat_{candidat.id}')
                if voix is not None and voix.isdigit():
                    Resultat.objects.update_or_create(
                        bureau_vote=bureau,
                        candidat=candidat,
                        defaults={'nombre_voix': int(voix)}
                    )
                    saved_count += 1
            
            messages.success(request, f"Résultats enregistrés pour le bureau {bureau.numero}")
            return redirect('elections:saisie_donnees')

        # Pré-remplir avec les résultats existants
        resultats_existants = {
            res.candidat_id: res.nombre_voix 
            for res in Resultat.objects.filter(bureau_vote=bureau)
        }
        
        candidats_form_data = []
        for cand in candidats:
            candidats_form_data.append({
                'candidat': cand,
                'voix': resultats_existants.get(cand.id, 0)
            })
            
        return render(request, 'elections/saisie_resultats.html', {
            'bureau': bureau,
            'candidats_data': candidats_form_data
        })


def resultats_globaux(request):
    """Vue principale des résultats globaux - Optimisée"""
    
    # 1. Totaux globaux (2 requêtes)
    total_voix = Resultat.objects.aggregate(total=Sum('nombre_voix'))['total'] or 0
    total_inscrits = BureauVote.objects.aggregate(total=Sum('nombre_inscrits'))['total'] or 0

    taux_participation = 0
    if total_inscrits > 0:
        taux_participation = round((total_voix / total_inscrits) * 100, 2)

    # 2. Candidats avec leurs voix (1 requête)
    candidats = Candidat.objects.annotate(
        voix=Coalesce(Sum('resultats__nombre_voix'), 0)
    ).order_by('-voix')

    # 3. Construction des données
    resultats_candidats = []
    for candidat in candidats:
        pourcentage = 0
        if total_voix > 0:
            pourcentage = round((candidat.voix / total_voix) * 100, 2)
            
        resultats_candidats.append({
            'candidat': candidat,
            'voix': candidat.voix,
            'pourcentage': pourcentage
        })

    context = {
        'resultats_candidats': resultats_candidats,
        'total_voix': total_voix,
        'total_inscrits': total_inscrits,
        'taux_participation': taux_participation,
    }

    return render(request, 'elections/resultats_globaux.html', context)


def resultats_par_centre(request):
    """Résultats détaillés par centre de vote - Optimisée"""
    # Récupérer tous les candidats une fois
    candidats = list(Candidat.objects.all())
    
    # Récupérer tous les centres
    centres = CentreVote.objects.all()

    # Aggrégation des inscrits par centre
    inscrits_map = {
        item['centre']: item['total'] 
        for item in BureauVote.objects.values('centre').annotate(total=Sum('nombre_inscrits'))
    }

    # Aggrégation des voix par centre (total)
    voix_centre_map = {
        item['bureau_vote__centre']: item['total']
        for item in Resultat.objects.values('bureau_vote__centre').annotate(total=Sum('nombre_voix'))
    }

    # Aggrégation des voix par (centre, candidat)
    details_map = {
        (item['bureau_vote__centre'], item['candidat']): item['total']
        for item in Resultat.objects.values('bureau_vote__centre', 'candidat').annotate(total=Sum('nombre_voix'))
    }

    centres_data = []
    for centre in centres:
        total_voix_centre = voix_centre_map.get(centre.id, 0)
        total_inscrits_centre = inscrits_map.get(centre.id, 0)
        
        resultats_centre = []
        for cand in candidats:
            voix = details_map.get((centre.id, cand.id), 0)
            pourcentage = 0
            if total_voix_centre > 0:
                pourcentage = round((voix / total_voix_centre) * 100, 2)
            
            resultats_centre.append({
                'candidat': cand,
                'voix': voix,
                'pourcentage': pourcentage
            })
            
        # Tri des résultats du centre
        resultats_centre.sort(key=lambda x: x['voix'], reverse=True)

        centres_data.append({
            'centre': centre,
            'resultats': resultats_centre,
            'total_voix': total_voix_centre,
            'total_inscrits': total_inscrits_centre
        })

    context = {
        'centres_data': centres_data
    }

    return render(request, 'elections/resultats_par_centre.html', context)


def resultats_par_bureau(request):
    """Résultats détaillés de tous les bureaux - Optimisée"""
    candidats = list(Candidat.objects.all().order_by('numero'))
    
    # Optimisation: Charger bureaux + centre en une fois
    bureaux = BureauVote.objects.select_related('centre').all()

    # Map des voix par bureau (total)
    voix_bureau_map = {
        item['bureau_vote']: item['total']
        for item in Resultat.objects.values('bureau_vote').annotate(total=Sum('nombre_voix'))
    }

    # Map des résultats détaillés (bureau, candidat)
    details_map = {
        (item['bureau_vote'], item['candidat']): item['nombre_voix']
        for item in Resultat.objects.values('bureau_vote', 'candidat', 'nombre_voix')
    }

    bureaux_data = []
    for bureau in bureaux:
        total_voix_bureau = voix_bureau_map.get(bureau.id, 0)
        
        resultats_bureau = []
        for cand in candidats:
            voix = details_map.get((bureau.id, cand.id), 0)
            pourcentage = 0
            if total_voix_bureau > 0:
                pourcentage = round((voix / total_voix_bureau) * 100, 2)
            
            resultats_bureau.append({
                'candidat': cand,
                'voix': voix,
                'pourcentage': pourcentage
            })

        # Trouver le gagnant
        gagnant = max(resultats_bureau, key=lambda x: x['voix']) if resultats_bureau and total_voix_bureau > 0 else None
        
        # Calcul taux participation
        taux_part = 0
        if bureau.nombre_inscrits > 0:
            taux_part = round((total_voix_bureau / bureau.nombre_inscrits) * 100, 2)

        bureaux_data.append({
            'bureau': bureau,
            'resultats': resultats_bureau,
            'total_voix': total_voix_bureau,
            'taux_participation': taux_part,
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
    
    # Optimisation: charger resultats et candidat en une fois
    resultats = Resultat.objects.filter(bureau_vote=bureau).select_related('candidat')
    
    total_voix = resultats.aggregate(total=Sum('nombre_voix'))['total'] or 0

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
    
    taux_part = 0
    if bureau.nombre_inscrits > 0:
        taux_part = round((total_voix / bureau.nombre_inscrits) * 100, 2)

    context = {
        'bureau': bureau,
        'resultats': resultats_data,
        'total_voix': total_voix,
        'taux_participation': taux_part
    }

    return render(request, 'elections/detail_bureau.html', context)


# --- Gestion Candidats ---
def liste_candidats(request):
    candidats = Candidat.objects.all()
    return render(request, 'elections/gestion/liste_candidats.html', {'candidats': candidats})

def ajouter_candidat(request):
    form = CandidatForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Candidat ajouté avec succès !")
        return redirect('elections:liste_candidats')
    return render(request, 'elections/gestion/form_generique.html', {'form': form, 'titre': 'Ajouter un Candidat'})

def modifier_candidat(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    form = CandidatForm(request.POST or None, request.FILES or None, instance=candidat)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Candidat modifié avec succès !")
        return redirect('elections:liste_candidats')
    return render(request, 'elections/gestion/form_generique.html', {'form': form, 'titre': 'Modifier le Candidat'})

def supprimer_candidat(request, pk):
    candidat = get_object_or_404(Candidat, pk=pk)
    if request.method == 'POST':
        candidat.delete()
        messages.success(request, "Candidat supprimé !")
        return redirect('elections:liste_candidats')
    return render(request, 'elections/gestion/confirm_delete.html', {'objet': candidat, 'type': 'Candidat'})


# --- Gestion Centres ---
def liste_centres(request):
    centres = CentreVote.objects.all()
    return render(request, 'elections/gestion/liste_centres.html', {'centres': centres})

def ajouter_centre(request):
    form = CentreVoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Centre ajouté avec succès !")
        return redirect('elections:liste_centres')
    return render(request, 'elections/gestion/form_generique.html', {'form': form, 'titre': 'Ajouter un Centre'})

def modifier_centre(request, pk):
    centre = get_object_or_404(CentreVote, pk=pk)
    form = CentreVoteForm(request.POST or None, instance=centre)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Centre modifié avec succès !")
        return redirect('elections:liste_centres')
    return render(request, 'elections/gestion/form_generique.html', {'form': form, 'titre': 'Modifier le Centre'})

def supprimer_centre(request, pk):
    centre = get_object_or_404(CentreVote, pk=pk)
    if request.method == 'POST':
        centre.delete()
        messages.success(request, "Centre supprimé !")
        return redirect('elections:liste_centres')
    return render(request, 'elections/gestion/confirm_delete.html', {'objet': centre, 'type': 'Centre'})


# --- Gestion Bureaux ---
def liste_bureaux(request):
    bureaux = BureauVote.objects.select_related('centre').all()
    return render(request, 'elections/gestion/liste_bureaux.html', {'bureaux': bureaux})

def ajouter_bureau(request):
    form = BureauVoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Bureau ajouté avec succès !")
        return redirect('elections:liste_bureaux')
    return render(request, 'elections/gestion/form_generique.html', {'form': form, 'titre': 'Ajouter un Bureau'})

def modifier_bureau(request, pk):
    bureau = get_object_or_404(BureauVote, pk=pk)
    form = BureauVoteForm(request.POST or None, instance=bureau)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Bureau modifié avec succès !")
        return redirect('elections:liste_bureaux')
    return render(request, 'elections/gestion/form_generique.html', {'form': form, 'titre': 'Modifier le Bureau'})

def supprimer_bureau(request, pk):
    bureau = get_object_or_404(BureauVote, pk=pk)
    if request.method == 'POST':
        bureau.delete()
        messages.success(request, "Bureau supprimé !")
        return redirect('elections:liste_bureaux')
    return render(request, 'elections/gestion/confirm_delete.html', {'objet': bureau, 'type': 'Bureau'})



