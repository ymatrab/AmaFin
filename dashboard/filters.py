
# filters.py
import django_filters
from .models import Achat, Escompte

class AchatFilter(django_filters.FilterSet):
    class Meta:
        model = Achat
        fields = {
            'banque': ['exact'],
            'societe': ['exact'],
            'document': ['exact'],
        }

class EscompteFilter(django_filters.FilterSet):
    class Meta:
        model = Escompte
        fields = {
            'banque': ['exact'],
            'escompte': ['exact'],
            'code_client': ['exact'],
            'date_decal': ['gte', 'lte'],
            'date_de_payement': ['gte', 'lte'],
        }