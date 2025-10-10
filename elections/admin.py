from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Candidat, CentreVote, BureauVote, Resultat


class ResultatInline(admin.TabularInline):
    model = Resultat
    extra = 1
    fields = ['candidat', 'nombre_voix', 'pourcentage_bureau']
    readonly_fields = ['pourcentage_bureau']

    def pourcentage_bureau(self, obj):
        if obj.id:
            return f"{obj.pourcentage_bureau()}%"
        return "-"

    pourcentage_bureau.short_description = "Pourcentage"


class BureauVoteInline(admin.TabularInline):
    model = BureauVote
    extra = 1
    fields = ['numero', 'nombre_inscrits', 'voir_details']
    readonly_fields = ['voir_details']

    def voir_details(self, obj):
        if obj.id:
            url = reverse('admin:elections_bureauvote_change', args=[obj.id])
            return format_html('<a href="{}" class="button">Modifier ✏️</a>', url)
        return "-"

    voir_details.short_description = "Actions"


@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nom', 'prenom', 'parti', 'total_voix', 'pourcentage_global', 'modifier']
    list_filter = ['parti']
    search_fields = ['nom', 'prenom']
    list_editable = ['nom', 'prenom', 'parti']
    ordering = ['numero']

    def modifier(self, obj):
        url = reverse('admin:elections_candidat_change', args=[obj.id])
        return format_html('<a href="{}" class="button">✏️ Modifier</a>', url)

    modifier.short_description = "Actions"


@admin.register(CentreVote)
class CentreVoteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'commune', 'total_inscrits', 'total_voix', 'nombre_bureaux', 'modifier']
    list_filter = ['commune']
    search_fields = ['nom', 'commune']
    inlines = [BureauVoteInline]
    list_editable = ['commune']

    def nombre_bureaux(self, obj):
        count = obj.bureaux.count()
        return f"{count} bureau{'x' if count > 1 else ''}"

    nombre_bureaux.short_description = "Bureaux"

    def modifier(self, obj):
        url = reverse('admin:elections_centrevote_change', args=[obj.id])
        return format_html('<a href="{}" class="button">✏️ Modifier</a>', url)

    modifier.short_description = "Actions"


@admin.register(BureauVote)
class BureauVoteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'centre', 'nombre_inscrits', 'total_voix', 'taux_participation', 'modifier']
    list_filter = ['centre__commune', 'centre']
    search_fields = ['numero', 'centre__nom']
    inlines = [ResultatInline]
    list_editable = ['nombre_inscrits']

    fieldsets = (
        ('Informations du Bureau', {
            'fields': ('centre', 'numero', 'nombre_inscrits')
        }),
        ('Statistiques', {
            'fields': ('total_voix_display', 'taux_participation_display'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['total_voix_display', 'taux_participation_display']

    def total_voix_display(self, obj):
        if obj.id:
            return obj.total_voix()
        return 0

    total_voix_display.short_description = "Total des voix"

    def taux_participation_display(self, obj):
        if obj.id:
            return f"{obj.taux_participation()}%"
        return "0%"

    taux_participation_display.short_description = "Taux de participation"

    def modifier(self, obj):
        url = reverse('admin:elections_bureauvote_change', args=[obj.id])
        return format_html('<a href="{}" class="button">✏️ Modifier</a>', url)

    modifier.short_description = "Actions"


@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ['candidat', 'bureau_vote', 'nombre_voix', 'pourcentage_bureau', 'modifier']
    list_filter = ['candidat', 'bureau_vote__centre__commune', 'bureau_vote__centre']
    search_fields = ['candidat__nom', 'bureau_vote__numero']
    list_editable = ['nombre_voix']

    fieldsets = (
        ('Informations', {
            'fields': ('candidat', 'bureau_vote', 'nombre_voix')
        }),
        ('Statistiques', {
            'fields': ('pourcentage_display',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['pourcentage_display']

    def pourcentage_display(self, obj):
        if obj.id:
            return f"{obj.pourcentage_bureau()}%"
        return "0%"

    pourcentage_display.short_description = "Pourcentage dans le bureau"

    def modifier(self, obj):
        url = reverse('admin:elections_resultat_change', args=[obj.id])
        return format_html('<a href="{}" class="button">✏️ Modifier</a>', url)

    modifier.short_description = "Actions"


# Configuration du site admin
admin.site.site_header = "🗳️ Administration des Élections"
admin.site.site_title = "Gestion Élections"
admin.site.index_title = "Tableau de bord des élections"