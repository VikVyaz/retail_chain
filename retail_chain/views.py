from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError

from retail_chain.models import Product, SupplyChainNode
from retail_chain.serializers import ProductSerializer, NodeSerializer, NodeUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = SupplyChainNode.objects.all()

    def perform_create(self, serializer):
        data = serializer.validated_data

        role = data['supply_chain_role']
        supplier = None
        if role == 'factory':
            chain_level = 0
        else:
            supplier = data['supplier']
            chain_level = supplier.chain_level + 1
        serializer.save(chain_level=chain_level, supplier=supplier)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NodeUpdateSerializer
        return NodeSerializer
