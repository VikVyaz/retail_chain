import django_filters

from .models import SupplyChainNode


class NodeFilter(django_filters.FilterSet):
    """Фильтр для поиска по стране у SupplyChainNode"""

    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')

    class Meta:
        model = SupplyChainNode
        fields = ('country',)
