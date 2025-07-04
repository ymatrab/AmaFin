from django.db.models import Sum
from collections import defaultdict
from datetime import timedelta, date, datetime
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



# def get_daily_series(payment_types, today):
#     seven_days_later = today + timedelta(days=6)

#     categories = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
#     daily_data_by_type = {ptype: defaultdict(float) for ptype in payment_types}

#     for ptype in payment_types:
#         if ptype == 'courant':
#             raw_achats = Achat.objects.filter(
#                 date_debit__isnull=False,
#                 date_debit__range=[ today, seven_days_later],
#                 debit=False,
#                 payment_type='courant'
#             ).values('date_debit', 'montant_dhs')
            
#             for achat in raw_achats:
#                 date_str = achat['date_debit'].strftime('%Y-%m-%d')
#                 daily_data_by_type['courant'][date_str] += float(achat['montant_dhs'])

#         elif ptype == 'finex':
#             raw_achats = Achat.objects.filter(
#                 date_echeance_finex__isnull=False,
#                 date_echeance_finex__range=[today,seven_days_later],
#                 statut_finex='exécute',
#                 payment_type='finex'
#             ).values('date_echeance_finex', 'montant_dhs')
            
#             for achat in raw_achats:
#                 date_str = achat['date_echeance_finex'].strftime('%Y-%m-%d')
#                 daily_data_by_type['finex'][date_str] += float(achat['montant_dhs'])

#         elif ptype == 'effet':
#             raw_achats = Achat.objects.filter(
#                 date_echeance_effet__isnull=False,
#                 date_echeance_effet__range=[today,seven_days_later],
#                 debit=False,
#                 payment_type='effet'
#             ).values('date_echeance_effet', 'montant_dhs')
            
#             for achat in raw_achats:
#                 date_str = achat['date_echeance_effet'].strftime('%Y-%m-%d')
#                 daily_data_by_type['effet'][date_str] += float(achat['montant_dhs'])

#     series = []
#     for ptype in payment_types:
#         data = [daily_data_by_type[ptype].get(day, 0) / 1_000_000 for day in categories]
#         series.append({
#             'name': ptype.capitalize(),
#             'data': data
#         })

#     return series, categories


from collections import defaultdict
from datetime import timedelta

def get_daily_series(payment_types, today):
    categories = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    daily_data_by_type = {ptype: defaultdict(float) for ptype in payment_types}

    for ptype in payment_types:
        for i in range(7):
            current_day = today + timedelta(days=i)
            day_str = current_day.strftime('%Y-%m-%d')

            if ptype == 'courant':
                if i == 0:  # today
                    raw_achats = Achat.objects.filter(
                        date_debit__isnull=False,
                        date_debit__lte=current_day,
                        debit=False,
                        payment_type='courant'
                    ).values('montant_dhs')
                else:
                    raw_achats = Achat.objects.filter(
                        date_debit__isnull=False,
                        date_debit=current_day,
                        debit=False,
                        payment_type='courant'
                    ).values('montant_dhs')

            elif ptype == 'finex':
                if i == 0:
                    raw_achats = Achat.objects.filter(
                        date_echeance_finex__isnull=False,
                        date_echeance_finex__lte=current_day,
                        statut_finex='exécute',
                        payment_type='finex'
                    ).values('montant_dhs')
                else:
                    raw_achats = Achat.objects.filter(
                        date_echeance_finex=current_day,
                        statut_finex='exécute',
                        payment_type='finex'
                    ).values('montant_dhs')

            elif ptype == 'effet':
                if i == 0:
                    raw_achats = Achat.objects.filter(
                        date_echeance_effet__isnull=False,
                        date_echeance_effet__lte=current_day,
                        debit=False,
                        payment_type='effet'
                    ).values('montant_dhs')
                else:
                    raw_achats = Achat.objects.filter(
                        date_echeance_effet=current_day,
                        debit=False,
                        payment_type='effet'
                    ).values('montant_dhs')

            total = sum(float(achat['montant_dhs']) for achat in raw_achats)
            daily_data_by_type[ptype][day_str] += total

    series = []
    for ptype in payment_types:
        data = [daily_data_by_type[ptype].get(day, 0) / 1_000_000 for day in categories]
        series.append({
            'name': ptype.capitalize(),
            'data': data
        })

    return series, categories


def get_weekly_series(payment_types, today):
    if isinstance(today, str):
        today = datetime.strptime(today, "%Y-%m-%d").date()

    # 🔁 4 semaines avant + semaine actuelle + 13 semaines après = 18 semaines
    start_of_current_week = today - timedelta(days=today.weekday())
    week_starts = [(start_of_current_week - timedelta(weeks=4)) + timedelta(weeks=i) for i in range(18)]
    week_labels = [d.strftime('%Y-%m-%d') for d in week_starts]

    data_par_type = {ptype: defaultdict(float) for ptype in payment_types}

    for ptype in payment_types:
        for i, week_start in enumerate(week_starts):
            week_end = week_start + timedelta(days=6)  # fin de la semaine (dimanche)
            week_label = week_start.strftime('%Y-%m-%d')

            if ptype == 'courant':
                raw_achats = Achat.objects.filter(
                    date_debit__isnull=False,
                    date_debit__range=[week_start, week_end],
                    debit=False,
                    payment_type='courant'
                ).values('montant_dhs')

            elif ptype == 'finex':
                raw_achats = Achat.objects.filter(
                    date_echeance_finex__isnull=False,
                    date_echeance_finex__range=[week_start, week_end],
                    statut_finex='exécute',
                    payment_type='finex'
                ).values('montant_dhs')

            elif ptype == 'effet':
                raw_achats = Achat.objects.filter(
                    date_echeance_effet__isnull=False,
                    date_echeance_effet__range=[week_start, week_end],
                    debit=False,
                    payment_type='effet'
                ).values('montant_dhs')

            total = sum(float(achat['montant_dhs']) for achat in raw_achats)
            data_par_type[ptype][week_label] += total

    series = []
    for ptype in payment_types:
        data = [data_par_type[ptype].get(label, 0) / 1_000_000 for label in week_labels]
        series.append({
            'name': ptype.capitalize(),
            'data': data
        })

    return series, week_labels



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
                statut_finex='exécute'
            )
            .aggregate(total=Sum('montant_dhs'))['total'] or 0
        )
        montant_planifie =  (
            Achat.objects
            .filter(
                payment_type='finex',
                banque=banque,
                date_paiement_fournisseur__lte=today,
                statut_finex='planifie'
            )
            .aggregate(total=Sum('montant_dhs'))['total'] or 0
        )

        resultats.append({
            'banque': banque.banque,
            'montant_consomme': float(montant_consomme),
            'montant_planifie': float(montant_planifie),
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
