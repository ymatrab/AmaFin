from django.db.models import Sum
from django.utils.timezone import now
from django.db.models.functions import TruncWeek
from collections import defaultdict
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import timedelta, date
from .models import Achat, Solde, Income, Escompte, Bank


def get_total_solde(today):
    return Solde.objects.filter(Solde_date=today).aggregate(total=Sum('montant_dhs'))['total'] or 0


def get_total_encaissement(today):
    return Income.objects.filter(date_Income=today).aggregate(total=Sum('montant'))['total'] or 0


def get_total_achat_urgent():
    return Achat.objects.filter(
        payment_type='courant',
        priority=0,
        debit=False
    ).aggregate(total=Sum('montant_dhs'))['total'] or 0


def get_top_achats():
    return list(
        Achat.objects
        .filter(payment_type='courant', priority=0, debit=False)
        .order_by('-montant_dhs')[:15]
        .values('fournisseurs', 'montant_dhs')
    )


def get_daily_series(payment_types, today):
    seven_days_ago = today - timedelta(days=6)
    daily_data_by_type = {ptype: defaultdict(float) for ptype in payment_types}

    raw_achats = Achat.objects.filter(
        date_debit__isnull=False,
        date_debit__range=[seven_days_ago, today],
        debit=False,
        payment_type__in=payment_types
    ).values('date_debit', 'montant_dhs', 'payment_type')

    for achat in raw_achats:
        date_str = achat['date_debit'].strftime('%Y-%m-%d')
        ptype = achat['payment_type']
        daily_data_by_type[ptype][date_str] += float(achat['montant_dhs'])

    categories = [(seven_days_ago + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    series = []
    for ptype in payment_types:
        data = [daily_data_by_type[ptype].get(day, 0) / 1_000_000 for day in categories]
        series.append({
            'name': ptype.capitalize(),
            'data': data
        })
    return series, categories


def get_weekly_series(payment_types, today):
    
    today = now().date()
    # Ancrer le début sur le lundi de la semaine actuelle moins 17 semaines
    start_of_current_week = today - timedelta(days=today.weekday())
    first_week_start = start_of_current_week  - timedelta(weeks=4)

    
    achats_hebdomadaires_bruts = (
        Achat.objects
        .filter(
            date_debit__isnull=False,
            date_debit__gte=first_week_start,
            debit=False,
            payment_type__in=payment_types
        )
        .annotate(week=TruncWeek('date_debit'))
        .values('week', 'payment_type')
        .annotate(total_hebdo=Sum('montant_dhs'))
        .order_by('week')
    )

    # 🗓️ On utilise directement les dates des lundis comme étiquettes
    weeks_labels = [(first_week_start + timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(18)]
    
    data_par_type_hebdo = {ptype: {week: 0.0 for week in weeks_labels} for ptype in payment_types}

    for item in achats_hebdomadaires_bruts:
        # 🔄 Convertit la semaine (datetime) en string de date (lundi)
        semaine = item['week'].strftime('%Y-%m-%d')
        type_paiement = item['payment_type']
        montant = float(item['total_hebdo'])
        data_par_type_hebdo[type_paiement][semaine] += montant

    series_hebdomadaires = []
    for ptype in payment_types:
        valeurs = [data_par_type_hebdo[ptype][week] / 1_000_000 for week in weeks_labels]
        series_hebdomadaires.append({
            'name': ptype.capitalize(),
            'data': valeurs
        })

    return series_hebdomadaires, weeks_labels




def get_finex_consumption_by_bank():
    today = date.today()

    banques = Bank.objects.all()
    resultats = []

    for banque in banques:
        montant_consomme = (
            Achat.objects
            .filter(
                payment_type='finex',
                banque=banque,
                date_paiement_fournisseur__lte=today,
                date_echeance_finex__gte=today
            )
            .aggregate(total=Sum('montant_dhs'))['total'] or 0
        )

        resultats.append({
            'banque': banque.banque,
            'montant_consomme': float(montant_consomme),
            'limit_finex': float(banque.limit_finex or 0)
        })

    return resultats


def get_escompte_summary():
    banques = ['BMCE', 'BP']
    lignes_disponibles = {
        'BMCE': 4_000_000,
        'BP': 16_000_000
    }

    summary = {}

    for banque_nom in banques:
        # Total consommé : Libéré = False & escompte = 'OK'
        total_consommee = Escompte.objects.filter(
            banque__banque=banque_nom,
            Libere=False,
            escompte='OK'
        ).aggregate(total=Sum('montant_effet'))['total'] or 0

        # Total en cours : Libéré = False & escompte = 'En Cours'
        total_en_cours = Escompte.objects.filter(
            banque__banque=banque_nom,
            Libere=False,
            escompte='En Cours'
        ).aggregate(total=Sum('montant_effet'))['total'] or 0

        ligne_disponible = lignes_disponibles[banque_nom]
        disponible = ligne_disponible - total_en_cours - total_consommee

        summary[banque_nom] = {
            'total_consommee': total_consommee,
            'total_en_cours': total_en_cours,
            'ligne_disponible': ligne_disponible,
            'disponible': disponible
        }

    return summary
