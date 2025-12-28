from rest_framework import serializers

from retail_chain.models import Product, SupplyChainNode


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyChainNode
        fields = "__all__"
        read_only_fields = ('create_date', 'chain_level',)

    def validate(self, data):
        if data['supply_chain_role'] != 'factory' and data['supplier'] is None:
            raise serializers.ValidationError(
                {'supplier': 'Обязателен, если роль не factory'}
            )
        return data


class NodeUpdateSerializer(NodeSerializer):
    class Meta:
        model = SupplyChainNode
        fields = "__all__"
        read_only_fields = ('create_date', 'chain_level', 'debt')
