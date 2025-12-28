from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError

from retail_chain.filters import NodeFilter
from retail_chain.models import Product, SupplyChainNode, Factory
from retail_chain.serializers import ProductSerializer, NodeSerializer, NodeUpdateSerializer, FactorySerializer


class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.prefetch_related('produced_products').all()
    serializer_class = FactorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = SupplyChainNode.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NodeUpdateSerializer
        return NodeSerializer


class SearchByCountryView(generics.ListAPIView):
    serializer_class = NodeSerializer
    queryset = SupplyChainNode.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = NodeFilter
