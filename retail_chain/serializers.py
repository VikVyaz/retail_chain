from rest_framework import serializers

from retail_chain.models import Product, SupplyChainNode, Factory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_produced_by(self, value):
        if value is None:
            raise serializers.ValidationError(
                {'produced_by': 'Укажите завод-изготовитель'}
            )
        return value


class FactorySerializer(serializers.ModelSerializer):
    supply_chain_role = serializers.SerializerMethodField()
    chain_level = serializers.SerializerMethodField()
    produced_products = serializers.SerializerMethodField()

    class Meta:
        model = Factory
        fields = '__all__'
        read_only_fields = ('supply_chain_role', 'chain_level', 'produced_products', 'create_date')

    def get_supply_chain_role(self, obj):
        return 'factory'

    def get_chain_level(self, obj):
        return 0

    def get_produced_products(self, obj):
        queryset = obj.produced_products.all()
        return ProductSerializer(queryset, many=True).data


class NodeSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()
    chain_level = serializers.SerializerMethodField()

    class Meta:
        model = SupplyChainNode
        fields = "__all__"
        read_only_fields = ('create_date', 'chain_level', 'supplier')
        extra_kwargs = {
            'supplier_type': {'write_only': True},
            'supplier_id': {'write_only': True},
        }

    def get_supplier(self, obj):
        if obj.supplier_type == 'factory':
            return FactorySerializer(Factory.objects.get(id=obj.supplier_id)).data
        return NodeSerializer(SupplyChainNode.objects.get(id=obj.supplier_id)).data

    def get_chain_level(self, obj):
        supplier_obj = SupplyChainNode.objects.get(id=obj.supplier_id)
        return supplier_obj.chain_level + 1

    def validate(self, attrs):
        supplier_type = attrs.get('supplier_type')
        supplier_id = attrs.get('supplier_id')

        if supplier_type == 'factory':
            exists = Factory.objects.filter(id=supplier_id).exists()
        else:
            exists = SupplyChainNode.objects.filter(id=supplier_id).exists()

        if not exists:
            raise serializers.ValidationError({'supplier_id': 'Такого завода/поставщика не существует'})

        return attrs


class NodeUpdateSerializer(NodeSerializer):
    class Meta:
        model = SupplyChainNode
        fields = "__all__"
        read_only_fields = ('create_date', 'chain_level', 'supplier', 'debt')
