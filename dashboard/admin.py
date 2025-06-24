from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Engagement,Product,Bank, FX_Hist,Income,Achat, Impot, Salaire, Financement, Solde, Escompte
from .resources import InvoiceResource,EscompteResource
from .forms import EscompteForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Engagement)
class EngagementAdmin(ImportExportModelAdmin):
    list_display = (
        'priorite',
        'due_semaine',
        'commentaire',
        'date_debit',
        'debite',
        'semaine_debit',
        'p0_order',
        'is_p0',
        'payment_type',
        'date_paiement_fournisseur',
        'payment_semaine',
        'nb_jours_finex',
        'date_ech_finex',
        'ech_finex_semaine',
        'statut_finex',
        'montant',
        'devise',
        'fx_index',
        'rate',
        'taux',
        'taux_ajuste',
        'refinance_en_dh',
        'refinance_en_devise',
        'interet',
        'tx_interet',
        'interet_calcule',
        'difference',
        'theory_vs_real',
    )
    list_filter = (
        'priorite',
        'payment_type',
        'debite',
        'devise',
    )
    search_fields = (
        'commentaire',
        'p0_order',
        'statut_finex',
    )
    date_hierarchy = 'date_debit'


from .forms import AchatForm

@admin.register(Achat)
class AchatAdmin(ImportExportModelAdmin):
    form = AchatForm

    list_display = (
        "invoice_id",
        "date_enregistrement",
        "societe",
        "banque",
        "document",
        "fournisseurs",
        "numero_facture",
        "due_date",
        "montant",
        "devise",
        "montant_dhs",
        "commentaire",
        "payment_type","priority","debit","date_debit",
        "numero_effet","date_echeance_effet",
        "Finex","date_paiement_fournisseur","nb_jours_finex","date_echeance_finex","statut_finex",
        "interet","taux_interet","interet_calcule","difference",
        "refine_used","refinancement_type","formatted_percent_3m","formatted_taux","formatted_value_adjusted","refine_sugg"
    )
    list_filter = ("societe", "banque", "document", "debit","priority","payment_type")
    search_fields = ("fournisseurs", "numero_facture", "commentaire")
    date_hierarchy = "date_enregistrement"
    readonly_fields = ("invoice_id",)
    resource_class = InvoiceResource

    def formatted_percent_3m(self, obj):
        if obj.percent_3m is not None:
            return f"{obj.percent_3m * 100:.2f} %"
        return "-"
    formatted_percent_3m.short_description = 'Percent 3M'
    def formatted_taux(self, obj):
        if obj.taux is not None:
            return f"{obj.taux * 100:.2f}%"
        return "-"
    formatted_taux.short_description = 'Taux'

    def formatted_value_adjusted(self, obj):
        if obj.value_adjusted is not None:
            return f"{obj.value_adjusted * 100:.2f} %"
        return "-"
    formatted_value_adjusted.short_description = 'Value Ajustée'



@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('custom_id','banque', 'limit_finex', 'taux_interet_finex', 'interet_fix')
    search_fields = ('banque',)
    readonly_fields = ('custom_id',)
    list_filter = ('banque',)


@admin.register(FX_Hist)
class FX_HistAdmin(admin.ModelAdmin):
    list_display = (
        'fx_id', 'date', 'currency', 'refinancement_type','rate_actual', 'rate_fcst_3m',
        'formatted_percent_3m', 'formatted_vol_3m', 'formatted_value_adjusted',
    )

    readonly_fields = ('fx_id',)

    def formatted_percent_3m(self, obj):
        return f"{obj.percent_3m * 100:.2f} %"
    formatted_percent_3m.short_description = 'Percent 3M'

    def formatted_vol_3m(self, obj):
        return f"{obj.vol_3m * 100:.2f} %"
    formatted_vol_3m.short_description = 'Volatilité sur 3M'

    def formatted_value_adjusted(self, obj):
        return f"{obj.value_adjusted * 100:.2f} %"
    formatted_value_adjusted.short_description = 'Value Ajustée'

    # For editing: display raw values in form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['percent_3m'].label = "Percent 3M (ex: 0.035 for 3.5%)"
        return form

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'date_enregistrement', 'societe', 'document', 'banque',
        'formatted_montant'
    )
    list_filter = ('societe', 'document', 'banque')
    search_fields = ('societe',)

    def formatted_montant(self, obj):
        return f"{obj.montant:,.2f}"  # Use space or comma if needed
    formatted_montant.short_description = 'Montant'


@admin.register(Impot)
class ImpotAdmin(admin.ModelAdmin):
    list_display = (
        'date_enregistrement', 'societe', 'banque', 'document','montant_dhs',
        'date_debit', 'commentaire'
    )


@admin.register(Salaire)
class SalaireAdmin(admin.ModelAdmin):
    list_display = (
        'date_enregistrement', 'societe', 'banque', 'document','montant_dhs',
        'date_debit', 'commentaire'
    )


@admin.register(Financement)
class FinancementAdmin(admin.ModelAdmin):
    list_display = (
        'date_enregistrement', 'societe', 'banque', 'document',
        'date_debit',
        'montant', 'devise', 'montant_dhs', 'commentaire'
    )


@admin.register(Solde)
class SoldeAdmin(admin.ModelAdmin):
    list_display = ('date_enregistrement','Solde_date','societe', 'banque', 'montant_dhs')
    search_fields = ('banque','societe')
    date_hierarchy = 'Solde_date'
    list_filter = ('banque','societe')

@admin.register(Escompte)
class EscompteAdmin(ImportExportModelAdmin):
    form = EscompteForm

    list_display = [
        'escompte_id',
        'numero_effets',
        'n_remise', 
        'reference_en_bd',
        'date_decal',
        'code_client',
        'nom_client',
        'montant_effet',
        'date_decal_2',
        'escompte',
        'date_de_payement',
        'banque',
        'jours_retard',
        'jours_escompte',
        'formatted_libere',
        'formatted_cout',
        'date_creation'
    ]
    
    list_filter = [
        'escompte', 
        'banque', 
        'date_decal',
        'Libere',
        'date_creation'
    ]
    
    search_fields = [
        'numero_effets', 
        'nom_client', 
        'code_client',
        'reference_en_bd'
    ]
    
    readonly_fields = [
        'escompte_id',
        'escompte',
        'jours_retard', 
        'jours_escompte', 
        'Libere', 
        'le_cout',
        'date_creation'
    ]
    
    fieldsets = (
        ('Informations Principales', {
            'fields': (
                'escompte_id',
                'numero_effets',
                'n_remise', 
                'reference_en_bd'
            )
        }),
        ('Client', {
            'fields': (
                'code_client',
                'nom_client'
            )
        }),
        ('Dates et Montant', {
            'fields': (
                'date_decal',
                'date_decal_2',
                'date_de_payement',
                'montant_effet',
                'banque'
            )
        }),
        ('Calculs Automatiques', {
            'fields': (
                'escompte',
                'jours_retard',
                'jours_escompte', 
                'Libere',
                'le_cout'
            ),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        })
    )
    
    date_hierarchy = 'date_decal'
    ordering = ['-date_decal']
    resource_class = EscompteResource

    def formatted_libere(self, obj):
        if obj.Libere:
            return "✓ Libéré"
        return "⏳ En attente"
    formatted_libere.short_description = 'Statut Libération'

    def formatted_cout(self, obj):
        if obj.le_cout is not None:
            return f"{obj.le_cout:.2f} "
        return "-"
    formatted_cout.short_description = 'Coût'

from django.contrib import admin
from .models import TableUpdateStatus

@admin.register(TableUpdateStatus)
class TableUpdateStatusAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'last_update')
    ordering = ('-last_update',)
    search_fields = ('table_name',)



