# Python standard library
import json


# Django core imports
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import now

# Third-party imports
from django_tables2 import RequestConfig, SingleTableView


# Local application imports
from .filters import AchatFilter, EscompteFilter
from .forms import (
    AchatForm,
    BankForm,
    EscompteForm,
    FinancementForm,
    FXForm,
    ImpotsForm,
    IncomesForm,
    InvoiceFormSet,
    SalaireForm,
)
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
from .tables import (
    AchatTable,
    BankTable,
    EscompteTable,
    FinancementTable,
    FXTable,
    ImpotsTable,
    IncomesTable,
    InvoiceTable,
    SalaireTable,
)
from .utils import (
    get_daily_series,
    get_finex_consumption_by_bank,
    get_top_achats,
    get_total_achat_urgent,
    get_total_encaissement,
    get_total_solde,
    get_weekly_series,
    get_escompte_summary
)
from .services import recalculate_table_if_needed

from datetime import datetime

def home_view(request):
    today = now().date()
    #today = datetime.strptime("2025-07-05", "%Y-%m-%d").date()
    payment_types = ['courant', 'finex', 'effet']

    total_solde = get_total_solde(today)
    encaissement = get_total_encaissement(today)
    achat_urgent_total = get_total_achat_urgent()
    gap_p0 = total_solde + encaissement - achat_urgent_total
    top_achats_list = get_top_achats()

    daily_series, daily_categories = get_daily_series(payment_types, today)
    weekly_series, weekly_categories = get_weekly_series(payment_types, today)


    finex_par_banque = get_finex_consumption_by_bank()
    escompte_summary = get_escompte_summary()
    print("ESCOMPTE SUMMARY:", escompte_summary["BMCE"]['disponible'], escompte_summary["BP"]['disponible'])

    context = {
        'total_solde': total_solde,
        'encaissement': encaissement,
        'achat_urgent_total': achat_urgent_total,
        'gap_p0': gap_p0,
        'top_achats': top_achats_list,
        'top_achats_json': json.dumps(top_achats_list, cls=DjangoJSONEncoder),
        'daily_series_json': json.dumps(daily_series),
        'daily_categories_json': json.dumps(daily_categories),
        'weekly_series_json': json.dumps(weekly_series),
        'weekly_categories_json': json.dumps(weekly_categories),
        'finex_par_banque_json' : json.dumps(finex_par_banque),
        'escompte_disponible_BP': escompte_summary['BP']['disponible']/1000000,
        'escompte_disponible_BMCE': escompte_summary["BMCE"]['disponible']/1000000,
        'page_css': 'home.css',
    }
    return render(request, 'dashboard/home.html', context)

def factures(request):
    # Invoices formset
    if request.method == "POST":
        formset = InvoiceFormSet(request.POST, queryset=Achat.objects.all())
        if formset.is_valid():
            formset.save()
            return redirect("home")
    else:
        formset = InvoiceFormSet(queryset=Achat.objects.all())

    return render(request, "dashboard/invoices.html", {
        "formset": formset,
    })

class InvoiceListView(SingleTableView):
    model = Achat
    table_class = InvoiceTable
    template_name = 'dashboard/table.html'
    # filterset_class = InvoiceFilter
    paginate_by = 1000

# This view is for displaying the bank table=============
def bankView(request):
    banks = Bank.objects.all()
    return render(request, "dashboard/bank.html", {"banks": banks})

def bank_edit_view(request, pk):
    bank = get_object_or_404(Bank, pk=pk)
    form = BankForm(request.POST or None, instance=bank)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("bank-table")
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/bank-form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    
    table = BankTable(Bank.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "dashboard/bank.html", {"form": form, "table": table})

# This view is for displaying the FX table=============
def fx_table_view(request):
    form = FXForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("fx-table")

    table = FXTable(FX_Hist.objects.all().order_by("-date"))
    RequestConfig(request).configure(table)
    return render(request, "dashboard/FX_page.html", {"form": form, "table": table})

def fx_edit_view(request, pk):
    fx = get_object_or_404(FX_Hist, pk=pk)
    form = FXForm(request.POST or None, instance=fx)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("fx-table")

    # AJAX : renvoyer uniquement le formulaire HTML
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/fx_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Sinon : page complète fallback
    table = FXTable(FX_Hist.objects.all().order_by("-date"))
    RequestConfig(request).configure(table)
    return render(request, "dashboard/FX_page.html", {"form": form, "table": table})

def fx_delete_view(request, pk):
    fx = get_object_or_404(FX_Hist, pk=pk)
    fx.delete()
    return redirect("fx-table")

def fx_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = FXForm()
        html = render_to_string("dashboard/forms/fx_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    return JsonResponse({}, status=400)

# This view is for displaying the incomes table=============
def incomes_table_view(request):
    form = IncomesForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("incomes-table")

    table = IncomesTable(Income.objects.all().order_by("-date_enregistrement"))
    RequestConfig(request).configure(table)
    return render(request, "dashboard/incomes.html", {"form": form, "table": table})

def incomes_edit_view(request, pk):
    income = get_object_or_404(Income, pk=pk)
    form = IncomesForm(request.POST or None, instance=income)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("incomes-table")

    # AJAX : renvoyer uniquement le formulaire HTML
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/incomes_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Sinon : page complète fallback
    table = IncomesTable(Income.objects.all().order_by("-date_enregistrement"))
    RequestConfig(request).configure(table)
    return render(request, "dashboard/incomes.html", {"form": form, "table": table})

def incomes_delete_view(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    return redirect("incomes-table")

def incomes_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = IncomesForm()
        html = render_to_string("dashboard/forms/incomes_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    return JsonResponse({}, status=400)

# This view is for displaying the achats table=============
def achat_table_view(request):
    if request.method == "POST":
        form = AchatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("achat-table")
    else:
        form = AchatForm()

    achat_qs = Achat.objects.all().order_by("-date_enregistrement")
    achat_filter = AchatFilter(request.GET, queryset=achat_qs)
    achats  = achat_filter.qs

    return render(request, "dashboard/achat.html", {
        "form": form,
        "achats": achats,
        "filter": achat_filter
    })

def achat_edit_view(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    form = AchatForm(request.POST or None, instance=achat)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("achat-table")

    # If it's an AJAX GET (from the ✏️ button)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/achat_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Otherwise render full page (normal fallback)
    table = AchatTable(Achat.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "dashboard/achat.html", {"form": form, "table": table})

def achat_delete_view(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    achat.delete()
    return redirect("achat-table")

def achat_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = AchatForm()
        html = render_to_string("dashboard/forms/achat_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

# This view is for displaying the Impots table=============
def impots_table_view(request):
    form = ImpotsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("impots-table")

    # Pass impots queryset instead of table for the new template structure
    impots = Impot.objects.all().order_by("-date_enregistrement")
    return render(request, "dashboard/impots.html", {"form": form, "impots": impots})

def impots_edit_view(request, pk):
    impot = get_object_or_404(Impot, pk=pk)
    form = ImpotsForm(request.POST or None, instance=impot)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("impots-table")

    # AJAX : renvoyer uniquement le formulaire HTML
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/impot_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Sinon : page complète fallback
    impots = Impot.objects.all().order_by("-date_enregistrement")
    return render(request, "dashboard/impots.html", {"form": form, "impots": impots})

def impots_delete_view(request, pk):
    impot = get_object_or_404(Impot, pk=pk)
    impot.delete()
    return redirect("impots-table")

def impots_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = ImpotsForm()
        html = render_to_string("dashboard/forms/impot_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    return JsonResponse({}, status=400)

# This view is for displaying the salaires table=============

def salaires_table_view(request):
    form = SalaireForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("salaires-table")

    # If you use a manual table (as in your new structure), use:
    salaires = Salaire.objects.all().order_by("-date_enregistrement")
    return render(request, "dashboard/salaire.html", {"form": form, "salaires": salaires})

def salaires_edit_view(request, pk):
    salaire = get_object_or_404(Salaire, pk=pk)
    form = SalaireForm(request.POST or None, instance=salaire)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("salaires-table")

    # AJAX: return only the form HTML
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/salaire_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Fallback: full page
    salaires = Salaire.objects.all().order_by("-date_enregistrement")
    return render(request, "dashboard/salaire.html", {"form": form, "salaires": salaires})

def salaires_delete_view(request, pk):
    salaire = get_object_or_404(Salaire, pk=pk)
    salaire.delete()
    return redirect("salaires-table")

def salaires_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = SalaireForm()
        html = render_to_string("dashboard/forms/salaire_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    return JsonResponse({}, status=400)

# This view is for displaying the financement table=============

def financement_table_view(request):
    form = FinancementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("financement-table")

    # If you use a manual table (new structure), use:
    financements = Financement.objects.all().order_by("-date_enregistrement")
    return render(request, "dashboard/financement.html", {"form": form, "financements": financements})

    # If you still use django-tables2, keep:
    # table = FinancementTable(Financement.objects.all().order_by("-date_enregistrement"))
    # RequestConfig(request).configure(table)
    # return render(request, "dashboard/financement.html", {"form": form, "table": table})

def financement_edit_view(request, pk):
    financement = get_object_or_404(Financement, pk=pk)
    form = FinancementForm(request.POST or None, instance=financement)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("financement-table")

    # AJAX: return only the form HTML
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/financement_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Fallback: full page
    financements = Financement.objects.all().order_by("-date_enregistrement")
    return render(request, "dashboard/financement.html", {"form": form, "financements": financements})

def financement_delete_view(request, pk):
    financement = get_object_or_404(Financement, pk=pk)
    financement.delete()
    return redirect("financement-table")

def financement_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = FinancementForm()
        html = render_to_string("dashboard/forms/financement_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    return JsonResponse({}, status=400)


# This view is for displaying the escomptes table=============
from django.contrib.auth.decorators import permission_required

@permission_required('dashboard.view_escompte', raise_exception=True)
def escompte_table_view(request):
    recalculate_table_if_needed(
        table_name="Escompte",
        queryset=Escompte.objects.all(),
        update_fn=lambda obj: obj.calculate_fields(),
        update_fields=['le_cout', 'Libere', 'jours_escompte', 'jours_retard', 'escompte']
    )
    if request.method == "POST":
        form = EscompteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("escompte-table")
    else:
        form = EscompteForm()

    escompte_qs = Escompte.objects.all().order_by("-date_decal")
    escompte_filter = EscompteFilter(request.GET, queryset=escompte_qs)
    escomptes = escompte_filter.qs

    escompte_summary = get_escompte_summary()

    return render(request, "dashboard/escompte.html", {
        "form": form,
        "escomptes": escomptes,
        "filter": escompte_filter,
        'escompte_summary': escompte_summary
    })

@permission_required('dashboard.change_escompte', raise_exception=True)
def escompte_edit_view(request, pk):
    escompte = get_object_or_404(Escompte, pk=pk)
    form = EscompteForm(request.POST or None, instance=escompte)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("escompte-table")

    # If it's an AJAX GET (from the ✏️ button)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("dashboard/forms/escompte_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})

    # Otherwise render full page (normal fallback)
    table = EscompteTable(Escompte.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "dashboard/escompte.html", {"form": form, "table": table})

@permission_required('dashboard.delete_escompte', raise_exception=True)
def escompte_delete_view(request, pk):
    escompte = get_object_or_404(Escompte, pk=pk)
    escompte.delete()
    return redirect("escompte-table")

@permission_required('dashboard.add_escompte', raise_exception=True)
def escompte_create_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = EscompteForm()
        html = render_to_string("dashboard/forms/escompte_form.html", {"form": form}, request=request)
        return JsonResponse({"form_html": html})
    return JsonResponse({}, status=400)
