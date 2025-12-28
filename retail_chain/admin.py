from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Product, SupplyChainNode


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'release_date')


@admin.action(description='Очистить задолженность')
def clean_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(SupplyChainNode)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'supply_chain_role', 'country', 'city', 'supplier_link', 'chain_level')
    list_filter = ('city',)
    actions = (clean_debt,)

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:retail_chain_supplychainnode_change', args=[obj.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.title)
        return "-"

    supplier_link.short_description = "Поставщик"
    supplier_link.admin_order_field = "supplier"
