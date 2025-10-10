from django.db import models
from django.core.validators import MinValueValidator


class Candidat(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    parti = models.CharField(max_length=100, blank=True)
    numero = models.IntegerField(unique=True)
    photo = models.ImageField(upload_to='candidats/', blank=True, null=True)

    class Meta:
        ordering = ['numero']
        verbose_name_plural = "Candidats"

    def __str__(self):
        return f"{self.numero} - {self.prenom} {self.nom}"

    def total_voix(self):
        """Calcule le total des voix pour ce candidat"""
        return Resultat.objects.filter(candidat=self).aggregate(
            total=models.Sum('nombre_voix')
        )['total'] or 0

    def pourcentage_global(self):
        """Calcule le pourcentage global des voix"""
        total_voix_election = Resultat.objects.aggregate(
            total=models.Sum('nombre_voix')
        )['total'] or 0

        if total_voix_election == 0:
            return 0

        return round((self.total_voix() / total_voix_election) * 100, 2)


class CentreVote(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.TextField()
    commune = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Centres de vote"

    def __str__(self):
        return f"{self.nom} - {self.commune}"

    def total_voix(self):
        """Total des voix dans ce centre"""
        return Resultat.objects.filter(
            bureau_vote__centre=self
        ).aggregate(total=models.Sum('nombre_voix'))['total'] or 0

    def total_inscrits(self):
        """Total des inscrits dans ce centre"""
        return self.bureaux.aggregate(
            total=models.Sum('nombre_inscrits')
        )['total'] or 0


class BureauVote(models.Model):
    centre = models.ForeignKey(
        CentreVote,
        on_delete=models.CASCADE,
        related_name='bureaux'
    )
    numero = models.CharField(max_length=20)
    nombre_inscrits = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name_plural = "Bureaux de vote"
        unique_together = ['centre', 'numero']

    def __str__(self):
        return f"Bureau {self.numero} - {self.centre.nom}"

    def total_voix(self):
        """Total des voix dans ce bureau"""
        return self.resultats.aggregate(
            total=models.Sum('nombre_voix')
        )['total'] or 0

    def taux_participation(self):
        """Calcule le taux de participation"""
        if self.nombre_inscrits == 0:
            return 0
        return round((self.total_voix() / self.nombre_inscrits) * 100, 2)


class Resultat(models.Model):
    candidat = models.ForeignKey(
        Candidat,
        on_delete=models.CASCADE,
        related_name='resultats'
    )
    bureau_vote = models.ForeignKey(
        BureauVote,
        on_delete=models.CASCADE,
        related_name='resultats'
    )
    nombre_voix = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        verbose_name_plural = "Résultats"
        unique_together = ['candidat', 'bureau_vote']

    def __str__(self):
        return f"{self.candidat} - {self.bureau_vote}: {self.nombre_voix} voix"

    def pourcentage_bureau(self):
        """Pourcentage dans le bureau"""
        total_bureau = self.bureau_vote.total_voix()
        if total_bureau == 0:
            return 0
        return round((self.nombre_voix / total_bureau) * 100, 2)

