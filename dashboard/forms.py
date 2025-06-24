from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .models import Achat, Income, Bank, FX_Hist, Impot, Financement, Salaire, Escompte


InvoiceFormSet = modelformset_factory(
    Achat,
    fields="__all__",
    extra=1,  # toujours afficher une ligne vide pour créer un nouvel invoice
    widgets={
        "date_enregistrement": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        "societe": forms.Select(attrs={"class": "form-select"}),
        "banque": forms.Select(attrs={"class": "form-select"}),
        "document": forms.Select(attrs={"class": "form-select"}),
        "fournisseurs": forms.TextInput(attrs={"class": "form-control"}),
        "numero_facture": forms.TextInput(attrs={"class": "form-control"}),
        "montant": forms.NumberInput(attrs={"class": "form-control"}),
        "devise": forms.Select(attrs={"class": "form-select"}),
        "mt_dhs": forms.NumberInput(attrs={"class": "form-control"}),
        "commentaire": forms.TextInput(attrs={"class": "form-control"}),
    }
)

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = '__all__'
    def clean_invoice_id(self):
            invoice_id = self.cleaned_data['invoice_id']
            if self.instance.pk is None and Achat.objects.filter(invoice_id=invoice_id).exists():
                raise ValidationError("Un achat avec ce Code Facture existe déjà.")
            return invoice_id
    class Media:
        js = ('js/achat_payment_toggle.js',)

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["banque", "limit_finex", "taux_interet_finex", "interet_fix"]

class FXForm(forms.ModelForm):
    class Meta:
        model = FX_Hist
        fields = ["date", "currency", "rate_actual", "rate_fcst_3m", "percent_3m"]

class IncomesForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["date_Income","societe", "document", "banque", "montant"]

class ImpotsForm(forms.ModelForm):
    class Meta:
        model = Impot
        exclude = []

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        exclude = []

class FinancementForm(forms.ModelForm):
    class Meta:
        model = Financement
        exclude = []

class EscompteForm(forms.ModelForm):
    class Meta:
        model = Escompte
        fields = [
            'numero_effets',
            'n_remise', 
            'reference_en_bd',
            'date_decal',
            'code_client',
            'nom_client',
            'montant_effet',
            'date_decal_2',
            'date_de_payement',
            'banque'
        ]
        
    class Media:
        js = ('js/escompte_calculations.js',)
