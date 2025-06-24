from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import Achat, Bank, Escompte

class InvoiceResource(resources.ModelResource):
    banque = Field(
        column_name='banque',
        attribute='banque',
        widget=ForeignKeyWidget(Bank, 'banque')  # correspond à la colonne Bank.banque (ex: 'BP')
    )
    class Meta:
        model = Achat
        import_id_fields = ('id',)

    def before_save_instance(self, instance, row, **kwargs):
        instance.save()

class EscompteResource(resources.ModelResource):
    banque = Field(
        column_name='banque',
        attribute='banque',
        widget=ForeignKeyWidget(Bank, 'banque')  # correspond à la colonne Bank.banque (ex: 'BP')
    )
    class Meta:
        model = Escompte
        import_id_fields = ('id',)
    def before_save_instance(self, instance, row, **kwargs):
        instance.save()


