from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError

from retail_chain.filters import FactoryFilter, NodeFilter
from retail_chain.models import Factory, Product, SupplyChainNode
from retail_chain.serializers import (FactorySerializer, NodeSerializer,
                                      NodeUpdateSerializer, ProductSerializer)


class FactoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для Factory"""

    queryset = Factory.objects.prefetch_related('produced_products').all()
    serializer_class = FactorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Вьюсет для Product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class NodeViewSet(viewsets.ModelViewSet):
    """Вьюсет для SupplyChainNode"""

    queryset = SupplyChainNode.objects.all()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NodeUpdateSerializer
        return NodeSerializer


class SearchNodeByCountryView(generics.ListAPIView):
    """View для поиска по стране в SupplyChainNode"""

    serializer_class = NodeSerializer
    queryset = SupplyChainNode.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = NodeFilter


class SearchFactoryByCountryView(generics.ListAPIView):
    """View для поиска по стране в Factory"""

    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FactoryFilter
