from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Product, SupplyChainNode, Factory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для Product"""

    list_display = ('title', 'model', 'release_date')


@admin.action(description='Очистить задолженность')
def clean_debt(modeladmin, request, queryset):
    """admin-action для обнуления долга"""

    queryset.update(debt=0)


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    """Админ-панель для Factory"""

    list_display = ('title', 'supply_chain_role', 'country', 'city', 'chain_level')
    list_filter = ('city',)

    def supply_chain_role(self, obj):
        return 'factory'

    supply_chain_role.short_description = 'Тип звена цепи поставок'


@admin.register(SupplyChainNode)
class NodeAdmin(admin.ModelAdmin):
    """Админ-панель для SupplyChainNode"""

    list_display = ('title', 'supply_chain_role', 'country', 'city', 'supplier_link', 'chain_level')
    list_filter = ('city',)
    actions = (clean_debt,)

    def supplier_link(self, obj):
        supplier = obj._supplier_obj
        if not supplier:
            return "-"

        if obj.supplier_type == 'factory':
            url = reverse('admin:retail_chain_factory_change', args=[supplier.pk])
        else:
            url = reverse('admin:retail_chain_supplychainnode_change', args=[supplier.pk])
        return format_html('<a href="{}">{}</a>', url, supplier.title)

    supplier_link.short_description = "Поставщик"
    supplier_link.admin_order_field = "supplier_id"
