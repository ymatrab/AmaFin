# Django core imports
from django.urls import reverse
from django.utils.html import format_html

# Third-party imports
import django_tables2 as tables

# Local imports
from .models import (
    Achat,
    Bank,
    Escompte,
    Financement,
    FX_Hist,
    Impot,
    Income,
    Salaire,
)


class InvoiceTable(tables.Table):
    class Meta:
        model = Achat
        template_name = "django_tables2/bootstrap.html"
        #fields = Invoice.Column()
    
class BankTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Bank
        template_name = "django_tables2/bootstrap5.html"
        fields = ("custom_id", "banque", "limit_finex", "taux_interet_finex", "interet_fix")

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a>',
            reverse("bank-edit", args=[record.pk]),
        )

class FXTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = FX_Hist
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "fx_id", "date", "currency", "rate_actual", "rate_fcst_3m",
            "percent_3m", "vol_3m", "value_adjusted", "refinancement_type"
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("fx-edit", args=[record.pk]),
            reverse("fx-delete", args=[record.pk]),
        )

class IncomesTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Income
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "date_enregistrement","date_Income", "societe", "document", "banque", "montant"
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("incomes-edit", args=[record.pk]),
            reverse("incomes-delete", args=[record.pk]),
        )

class AchatTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Achat
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "invoice_id", "date_enregistrement", "societe", "banque",
            "document", "fournisseurs", "numero_facture", "due_date",
            "montant", "devise", "montant_dhs", "commentaire",
            "payment_type", "priority", "debit", "date_debit",
            "Finex", "date_paiement_fournisseur", "nb_jours_finex",
            "date_echeance_finex", "statut_finex", "interet",
            "taux_interet", "interet_calcule", "difference",
            "refinancement_type", "refine_used", "refine_sugg"
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("achat-edit", args=[record.pk]),
            reverse("achat-delete", args=[record.pk]),
        )

class ImpotsTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Impot
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "date_enregistrement", "societe", "banque", "document", "fournisseurs",
            "numero_facture", "due_date", "montant", "devise", "montant_dhs", "commentaire"
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("impots-edit", args=[record.pk]),
            reverse("impots-delete", args=[record.pk]),
        )

class SalaireTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Salaire
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "date_enregistrement", "societe", "banque", "document", "fournisseurs",
            "numero_facture", "due_date", "montant", "devise", "montant_dhs", "commentaire"
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("salaires-edit", args=[record.pk]),
            reverse("salaires-delete", args=[record.pk]),
        )

class FinancementTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Financement
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "date_enregistrement", "societe", "banque", "document", "fournisseurs",
            "numero_facture", "due_date", "montant", "devise", "montant_dhs", "commentaire"
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("financement-edit", args=[record.pk]),
            reverse("financement-delete", args=[record.pk]),
        )

class EscompteTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Actions")

    class Meta:
        model = Escompte
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "numero_effets", "n_remise", "reference_en_bd", "date_decal",
            "code_client", "nom_client", "montant_effet", "date_decal_2",
            "escompte", "date_de_payement", "banque", "jours_retard",
            "jours_escompte", "libere", "le_cout", 
        )

    def render_actions(self, record):
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}">✏️</a> '
            '<a class="btn btn-sm btn-danger" href="{}">🗑</a>',
            reverse("escompte-edit", args=[record.pk]),
            reverse("escompte-delete", args=[record.pk]),
        )
