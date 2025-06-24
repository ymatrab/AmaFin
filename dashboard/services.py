from datetime import date
from django.db import transaction
from .models import TableUpdateStatus, Escompte

@transaction.atomic
def recalculate_table_if_needed(table_name, queryset, update_fn, update_fields):
    from .models import TableUpdateStatus
    from datetime import date

    status, _ = TableUpdateStatus.objects.get_or_create(table_name=table_name)
    if status.last_update == date.today():
        return False

    for obj in queryset:
        update_fn(obj)
        obj.save(update_fields=update_fields)

    status.last_update = date.today()
    status.save(update_fields=['last_update'])
    return True



def recalculate_all_tables():
    from .models import Achat, FX_Hist, Escompte

    recalculate_table_if_needed(
        table_name="Escompte",
        queryset=Escompte.objects.all(),
        update_fn=lambda obj: obj.calculate_fields(),
        update_fields=['le_cout', 'Libere', 'jours_escompte', 'jours_retard', 'escompte']
    )

    recalculate_table_if_needed(
        table_name="Achat",
        queryset=Achat.objects.all(),
        update_fn=lambda obj: obj.calculate_fields(),
        update_fields=['urgent']  # adapter selon tes champs
    )

    # recalculate_table_if_needed(
    #     table_name="FX_Hist",
    #     queryset=FX_Hist.objects.all(),
    #     update_fn=lambda obj: obj.calculate_fields(),
    #     update_fields=['adjusted']  # adapter selon tes champs
    # )
