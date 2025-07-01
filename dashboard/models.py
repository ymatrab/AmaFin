from django.db import models
from django.db.models import Max
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from datetime import timedelta , datetime, date


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name

class Bank(models.Model):
    custom_id = models.CharField(max_length=10, unique=True, editable=False)
    banque = models.CharField(max_length=100,unique=True)
    limit_finex = models.DecimalField(max_digits=30, decimal_places=5, null=True, blank=True)
    taux_interet_finex = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    interet_fix = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.custom_id:
            last_id = Bank.objects.all().order_by('-id').first()
            if last_id and last_id.custom_id.startswith('BK'):
                last_num = int(last_id.custom_id[2:])
                self.custom_id = f"BK{last_num + 1}"
            else:
                self.custom_id = "BK1"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.custom_id} - {self.banque}"

class FX_Hist(models.Model):
    CURRENCY_CHOICES = [('EUR', 'EUR'), ('USD', 'USD')]

    fx_id = models.CharField(max_length=10, unique=True, editable=False)
    date = models.DateField()
    currency = models.CharField(choices=CURRENCY_CHOICES)
    rate_actual = models.DecimalField(max_digits=30, decimal_places=10)
    rate_fcst_3m = models.DecimalField(max_digits=30, decimal_places=10)
    percent_3m = models.DecimalField(max_digits=30, decimal_places=10)

    vol_3m = models.DecimalField(max_digits=30, decimal_places=10,editable=False)
    value_adjusted = models.DecimalField(max_digits=30, decimal_places=10,editable=False)
    refinancement_type = models.CharField(editable=False)

    def save(self, *args, **kwargs):
        # Auto-increment FX ID
        if not self.fx_id:
            last = FX_Hist.objects.order_by('-id').first()
            if last and last.fx_id.startswith('FX'):
                last_num = int(last.fx_id[2:])
                self.fx_id = f"FX{last_num + 1}"
            else:
                self.fx_id = "FX1"

        # Calculate volatility and adjusted value
        if self.rate_actual != 0:
            self.vol_3m = (self.rate_fcst_3m - self.rate_actual) / self.rate_actual
        else:
            self.vol_3m = 0
        # Refinancement Type
        if self.currency  == "EUR":
            self.refinancement_type = "EURIBOR"
        elif self.currency  == "USD":
            self.refinancement_type = "SOFR"
        else : 
            self.refinancement_type = ""

        self.value_adjusted = self.percent_3m + (self.vol_3m / 3 * 12)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fx_id} - {self.currency} - {self.date}"

class Achat(models.Model):
    invoice_id = models.IntegerField(
        "Code Facture", 
        unique=True, 
        editable=False,
    )
    date_enregistrement = models.DateField(default=now, editable=False)
    SOCIETE_CHOICES = [
        ('AMAD','AMAD'),
        ('FMCG','FMCG'),
        ('AMAP','AMAP'),
        ('SULFO','SULFO'),
        ('ENGINUP','ENGINUP'),
        ('ENOSIS','ENOSIS'),
        ('LAC','LAC'),
        ('TODAYWORKS','TODAYWORKS'),
        ('FMCG','FMCG'),
    ]
    societe = models.CharField("Société", max_length=50, choices=SOCIETE_CHOICES)
    BANQUE_CHOICES = [
        ('BP','BP'),
        ('BMCE','BMCE'),
        ('AWB','AWB'),
        ('CAM','CAM'),
    ]
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT, null=True, blank=True)

    DOCUMENT_CHOICES = [
        ('Facture','Facture'),
        ('Avance','Avance'),
    ]
    document = models.CharField("Document", max_length=50, choices=DOCUMENT_CHOICES)
    fournisseurs = models.CharField("Fournisseurs", max_length=255)
    numero_facture = models.CharField("N° de facture", max_length=100, blank=True)
    due_date = models.DateField("Due Date / Ech Facture",default=now, editable=True)
    montant = models.DecimalField("Montant", max_digits=12, decimal_places=2,blank=True, null=True,default=0)
    DEVIS_CHOICES = [
        ('EUR', 'EUR'),
        ('MAD','MAD'),
        ('USD','USD'),
    ]
    devise = models.CharField("Devise", max_length=10, choices=DEVIS_CHOICES,blank=True, null=True)
    montant_dhs = models.DecimalField("Montant DHS", max_digits=12, decimal_places=2,default=0,editable=None)
    commentaire = models.TextField("Commentaire", blank=True,null=True)
    PAYMENT_TYPES = [
        ('courant', 'Courant'),
        ('finex', 'Finex'),
        ('effet', 'Effet'),
    ]
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES,default='courant')
    # Courant fields
    PRIORITY_CHOICES = [
        (0, 'Priorité absolue (il faut payer immédiatement)'),
        (1, 'Priorité haute (à surveiller de près)'),
        (2, 'Priorité Normal'),
        (3, 'Non prioritaire'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    debit = models.BooleanField(default=False)
    date_debit = models.DateField(blank=True, null=True)
	

    # Finex fields
    Finex=models.CharField("Finex", max_length=50,default="-")
    date_paiement_fournisseur = models.DateField(default='1900-01-01')
    nb_jours_finex = models.IntegerField(default=0)
    date_echeance_finex = models.DateField(blank=True, null=True,editable=None) 
    STATUT_FINEX_CHOICES = [
        ('exécute', 'Exécuté'),
        ('paid', 'Payé'),
        ('planifie', 'Planifié'),
        ('initial', '-')
    ]
    statut_finex = models.CharField(max_length=20, choices=STATUT_FINEX_CHOICES, null=True, blank=True,default='initial',)
    interet = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,default=0)
    
    taux_interet = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True,editable=False)
    interet_calcule = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,editable=False)
    difference = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True,editable=False,default=0)


    # Effet fields
    numero_effet = models.CharField(max_length=100, blank=True, null=True)
    date_echeance_effet = models.DateField(blank=True, null=True)
    
    #refinancement
    REFINE_TYPE_CHOICES = [
        ('sofr', 'SOFR'),
        ('euribor', 'EURIBOR'),
        ('', 'NONE')
    ]

    refinancement_type = models.CharField(max_length=50, null=True, blank=True, editable=False)
    percent_3m = models.DecimalField(max_digits=30, decimal_places=10, null=True, blank=True, editable=False)
    taux = models.DecimalField(max_digits=30, decimal_places=10, null=True, blank=True, editable=False)
    value_adjusted = models.DecimalField(max_digits=30, decimal_places=10, null=True, blank=True, editable=False)
    refine_sugg = models.CharField(max_length=20, null=True, blank=True,default='',editable=None)

    REFINE_USED_CHOICES = [
        ('En DH', 'Refine en DH'),
        ('EN Devise', 'Refine en Devise'),
        ('', 'NONE')
    ]
    refine_used=models.CharField(max_length=20, choices=REFINE_USED_CHOICES,null=True, blank=True,default='-')

    def __str__(self):
        return f"{self.societe} – {self.numero_facture or '–'}"
    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_id = Achat.objects.aggregate(models.Max("invoice_id"))["invoice_id__max"] or 0
            print(f"Last invoice_id: {last_id}")
            self.invoice_id = last_id + 1

        if self.date_paiement_fournisseur and self.nb_jours_finex is not None:
            if isinstance(self.date_paiement_fournisseur, str):
                try:
                    self.date_paiement_fournisseur = datetime.strptime(self.date_paiement_fournisseur, "%Y-%m-%d").date()
                except ValueError:
                    self.date_paiement_fournisseur = date(1900, 1, 1)

            self.date_echeance_finex = self.date_paiement_fournisseur + timedelta(days=self.nb_jours_finex)

        if self.payment_type =="courant" :
            if not self.date_debit:
                self.date_debit=datetime.now()
            if self.devise =='MAD' :
                self.montant_dhs=self.montant
            elif self.devise in ['EUR', 'USD']:
                self.montant_dhs=self.montant * 11
        elif self.payment_type =="effet":
            self.date_echeance_effet=datetime.now()
            if self.devise =='MAD' :
                self.montant_dhs=self.montant
            elif self.devise in ['EUR', 'USD']:
                self.montant_dhs=self.montant * 11
        elif self.payment_type =="finex":
            if self.devise =='MAD' :
                self.refine_used="En DH"
                self.refine_sugg="En DH"
                self.montant_dhs=self.montant
                if self.banque is not None:
                    self.taux_interet = self.banque.interet_fix
            elif self.devise in ['EUR', 'USD']:
                fx = FX_Hist.objects.filter(
                    currency=self.devise,
                ).order_by('-date').first() 

                if fx:
                    self.montant_dhs=self.montant * fx.rate_actual
                    self.refinancement_type = fx.refinancement_type
                    self.percent_3m = fx.percent_3m
                    self.value_adjusted = fx.value_adjusted
                    if self.banque and self.banque.taux_interet_finex is not None:
                        self.taux = fx.percent_3m + self.banque.taux_interet_finex
                    if self.banque and self.banque.interet_fix is not None:
                        if self.value_adjusted > self.banque.interet_fix:
                            self.refine_sugg = "Refine en DH"
                        else:
                            self.refine_sugg = "Refine en Devise"
                if self.refine_used is not None and self.banque is not None:
                    if self.refine_used == "En DH":
                        self.taux_interet = self.banque.interet_fix
                    elif self.refine_used == "EN Devise":
                        self.taux_interet = self.value_adjusted
                    else:
                        self.taux_interet = 0
            if self.taux_interet is not None  :
                self.interet_calcule= self.taux_interet * self.nb_jours_finex * self.montant_dhs /360
            if self.interet_calcule is not None and self.interet is not None:
                self.difference = self.interet_calcule - self.interet
        super().save(*args, **kwargs)

class Engagement(models.Model):
    # 1-to-1 with Invoice (one engagement per invoice)
    invoice = models.OneToOneField(
        'dashboard.Achat',
        on_delete=models.CASCADE,
        related_name='engagement',
        verbose_name="Facture liée"
    )



    # new engagement-specific fields
    priorite          = models.PositiveSmallIntegerField("Priorité", validators=[MinValueValidator(0), MaxValueValidator(1)])
    due_semaine       = models.PositiveSmallIntegerField("Due Semaine")
    commentaire       = models.TextField("Commentaire", blank=True)

    # payment lifecycle
    date_debit        = models.DateField("DATE DEBIT / Date De Paiement", blank=True, null=True)
    debite            = models.BooleanField("Débité", default=False)
    semaine_debit     = models.PositiveSmallIntegerField("Semaine DEBIT", blank=True, null=True)

    p0_order          = models.CharField("P0 Order", max_length=50, blank=True)
    is_p0             = models.BooleanField("Is P0", default=False)

    PAYMENT_CHOICES = [
        ('regular', 'Regular'),
        ('finex',   'Finex'),
    ]
    payment_type      = models.CharField("Payment Type", max_length=10, choices=PAYMENT_CHOICES)

    # only for finex
    date_paiement_fournisseur = models.DateField("DATE Paiement Fournisseur", blank=True, null=True)
    payment_semaine           = models.PositiveSmallIntegerField("Payment Semaine", blank=True, null=True)
    nb_jours_finex            = models.PositiveSmallIntegerField("Nb Jours Finex", blank=True, null=True)
    date_ech_finex            = models.DateField("DATE ECH Finex", blank=True, null=True)
    ech_finex_semaine         = models.PositiveSmallIntegerField("Ech Finex Semaine", blank=True, null=True)
    statut_finex              = models.CharField("Statut Finex", max_length=50, blank=True)

    # refinancing & rates
    montant                   = models.DecimalField("Montant", max_digits=12, decimal_places=2)
    devise                    = models.CharField("Devise", max_length=10, choices=Achat.DEVIS_CHOICES)
    fx_index                  = models.CharField("SOFR / EURIBOR", max_length=20, blank=True)
    rate                      = models.DecimalField("Rate", max_digits=12, decimal_places=6, blank=True, null=True)
    taux                      = models.DecimalField("Taux", max_digits=12, decimal_places=6, blank=True, null=True)
    taux_ajuste               = models.DecimalField("TAUX AJUSTE", max_digits=12, decimal_places=6, blank=True, null=True)
    refinance_en_dh           = models.DecimalField("Refinance en DH", max_digits=14, decimal_places=2, blank=True, null=True)
    refinance_en_devise       = models.DecimalField("Refinance en Devise", max_digits=14, decimal_places=2, blank=True, null=True)

    # interest calculations
    interet                   = models.DecimalField("INTERET", max_digits=14, decimal_places=2, blank=True, null=True)
    tx_interet                = models.DecimalField("Tx intérêt (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    interet_calcule           = models.DecimalField("Intérêt Calculé", max_digits=14, decimal_places=2, blank=True, null=True)
    difference                = models.DecimalField("Difference", max_digits=14, decimal_places=2, blank=True, null=True)
    theory_vs_real            = models.DecimalField("Theory VS Real", max_digits=14, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Engagement"
        verbose_name_plural = "Engagements"

    def __str__(self):
        return f"Engagement {self.invoice.invoice_id}"

    def clean(self):
        # ensure finex-only fields are set when appropriate
        from django.core.exceptions import ValidationError
        if self.payment_type == 'finex':
            missing = []
            for fld in [
                'date_paiement_fournisseur', 'payment_semaine',
                'nb_jours_finex', 'date_ech_finex',
                'ech_finex_semaine', 'statut_finex'
            ]:
                if getattr(self, fld) in (None, ''):
                    missing.append(fld)
            if missing:
                raise ValidationError({fld: "Required for finex payments" for fld in missing})

class Income(models.Model):
    SOCIETE_CHOICES = [
        ('ENOSIS', 'ENOSIS'),
        ('AMAP', 'AMAP'),
        ('AMAD', 'AMAD'),
        ('SULFO', 'SULFO'),
        ('ENGINUP', 'ENGINUP'),
        ('FMCG', 'FMCG'),
        ('LAC', 'LAC'),
        ('TODAYWORKS', 'TODAYWORKS'),
    ]

    DOCUMENT_CHOICES = [
        ('Facture', 'Facture'),
        ('Avance', 'Avance'),
    ]

    date_enregistrement = models.DateField(default=now, editable=False)
    date_Income = models.DateField(default=now, )
    societe = models.CharField(max_length=20, choices=SOCIETE_CHOICES)
    document = models.CharField(max_length=10, choices=DOCUMENT_CHOICES)
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT)  # FK vers table Bank
    montant = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.societe} - {self.document} - {self.date_enregistrement}"

class Impot(models.Model):
    SOCIETE_CHOICES = [
        ('AMAD','AMAD'),
        ('FMCG','FMCG'),
        ('AMAP','AMAP'),
        ('SULFO','SULFO'),
        ('ENGINUP','ENGINUP'),
        ('ENOSIS','ENOSIS'),
        ('LAC','LAC'),
        ('TODAYWORKS','TODAYWORKS'),
    ]

    Document_CHOICES = [
        ('TVA','TVA'),
        ('Account IS','Account IS'),
    ]

    date_enregistrement = models.DateField(default=now, editable=False)
    societe = models.CharField(max_length=100, choices=SOCIETE_CHOICES)
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT)
    document = models.CharField(max_length=100,choices=Document_CHOICES)
    date_debit = models.DateField(blank=True, null=True)
    montant_dhs = models.DecimalField(max_digits=30, decimal_places=5)
    commentaire = models.TextField(blank=True, null=True)

class Salaire(models.Model):
    SOCIETE_CHOICES = [
        ('AMAD','AMAD'),
        ('FMCG','FMCG'),
        ('AMAP','AMAP'),
        ('SULFO','SULFO'),
        ('ENGINUP','ENGINUP'),
        ('ENOSIS','ENOSIS'),
        ('LAC','LAC'),
        ('TODAYWORKS','TODAYWORKS'),
    ]
    Document_CHOICES = [
        ('Paie','Paie'),
        ('CNSS','CNSS'),
        ('IR','IR'),
    ]
        

    date_enregistrement = models.DateField(default=now, editable=False)
    societe = models.CharField(max_length=100, choices=SOCIETE_CHOICES)
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT)
    document = models.CharField(max_length=100,choices=Document_CHOICES)
    date_debit = models.DateField(blank=True, null=True)
    montant_dhs = models.DecimalField(max_digits=30, decimal_places=5)
    commentaire = models.TextField(blank=True, null=True)

class Financement(models.Model):
    SOCIETE_CHOICES = [
        ('AMAD','AMAD'),
        ('FMCG','FMCG'),
        ('AMAP','AMAP'),
        ('SULFO','SULFO'),
        ('ENGINUP','ENGINUP'),
        ('ENOSIS','ENOSIS'),
        ('LAC','LAC'),
        ('TODAYWORKS','TODAYWORKS'),
    ]
    Document_CHOICES = [
        ('Credit','Credit'),
    ]
    

    date_enregistrement = models.DateField(default=now, editable=False)
    societe = models.CharField(max_length=100, choices=SOCIETE_CHOICES)
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT)
    document = models.CharField(max_length=100,choices=Document_CHOICES)
    date_debit = models.DateField(blank=True, null=True)
    montant = models.DecimalField(max_digits=30, decimal_places=5,blank=True, null=True)
    devise = models.CharField(max_length=10,blank=True, null=True)
    montant_dhs = models.DecimalField(max_digits=30, decimal_places=5)
    commentaire = models.TextField(blank=True, null=True)

class Solde(models.Model):
    date_enregistrement = models.DateField(default=now, editable=False)
    Solde_date = models.DateField(default=now)
    societe = models.CharField(max_length=100, choices=Achat.SOCIETE_CHOICES)
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT)
    montant_dhs = models.DecimalField(max_digits=30, decimal_places=5)

    def __str__(self):
        return f"{self.societe} - {self.banque} - {self.date_enregistrement}"
    
class Escompte(models.Model):
    SOCIETE_CHOICES = [
        ('ENOSIS', 'ENOSIS'),
        ('AMAP', 'AMAP'),
        ('AMAD', 'AMAD'),
        ('SULFO', 'SULFO'),
        ('ENGINUP', 'ENGINUP'),
        ('FMCG', 'FMCG'),
        ('LAC', 'LAC'),
        ('TODAYWORKS', 'TODAYWORKS'),
    ]

    ESCOMPTE_CHOICES = [
        ('OK', 'OK'),
        ('NOK', 'En Cours'),
    ]

    escompte_id = models.IntegerField(
        "Code Escompte", 
        unique=True, 
        editable=False,
    )

    # User Input Fields
    numero_effets = models.CharField(max_length=20)
    n_remise = models.CharField(max_length=20)
    reference_en_bd = models.CharField(max_length=50, blank=True, null=True)
    date_decal = models.DateField("date dépôt",default=now)
    code_client = models.CharField(max_length=20)
    nom_client = models.CharField(max_length=100)
    montant_effet = models.DecimalField(max_digits=20, decimal_places=2)
    date_decal_2 = models.DateField("Date d'effet",default=now)
    date_de_payement = models.DateField(null=True, blank=True,)
    banque = models.ForeignKey(Bank, on_delete=models.PROTECT)
    
    # Calculated Fields (auto-populated)
    escompte = models.CharField(max_length=10, choices=ESCOMPTE_CHOICES, blank=True)
    jours_retard = models.IntegerField(default=0, editable=False)
    jours_escompte = models.IntegerField(default=0, editable=False)
    Libere = models.BooleanField('Libéré',default=0, editable=False)
    le_cout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    
    # Metadata
    date_creation = models.DateTimeField(default=now, editable=False)

    class Meta:
        verbose_name = "Escompte"
        verbose_name_plural = "Escomptes"
        ordering = ['-date_decal']

    def calculate_fields(self):


        # Sécuriser les dates importées
        if isinstance(self.date_decal, datetime):
            self.date_decal = self.date_decal.date()
        if isinstance(self.date_decal_2, datetime):
            self.date_decal_2 = self.date_decal_2.date()
        if isinstance(self.date_de_payement, datetime):
            self.date_de_payement = self.date_de_payement.date()
        """Calculate derived fields based on input data"""
        today = datetime.now().date()
        
        if self.date_de_payement :
            self.escompte = 'OK'
        else:
            self.escompte = 'En Cours'

        if self.date_de_payement and self.date_decal and self.escompte == 'OK':
            self.jours_retard = max(0, (self.date_de_payement - self.date_decal ).days)

        if self.date_decal and self.date_decal_2:
            if self.escompte == 'OK':
                self.jours_escompte = abs((self.date_decal_2 - self.date_de_payement).days)
        
        if self.date_decal_2 < today:
            self.Libere = 1
        else: self.Libere = 0
        

        
        if self.jours_retard > 0 and self.montant_effet:
            rate = 0.05  # 0.1% per day
            self.le_cout = float(self.montant_effet) *self.jours_escompte / 365 * rate 
        else:
            self.le_cout = 0.00
    
    def save(self, *args, **kwargs):

        if not self.escompte_id:
            last_id = Escompte.objects.aggregate(models.Max("escompte_id"))["escompte_id__max"] or 0
            print(f"Last escompte_id: {last_id}")
            self.escompte_id = last_id + 1

        # Calculate fields before saving
        self.calculate_fields()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.numero_effets} - {self.nom_client} - {self.date_decal}"


class TableUpdateStatus(models.Model):
    table_name = models.CharField(max_length=100, unique=True)
    last_update = models.DateField(null=True, blank=True,editable=False)

    def __str__(self):
        return f"{self.table_name} - {self.last_update}"

