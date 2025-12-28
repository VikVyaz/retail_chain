from django.urls import path
from rest_framework.routers import DefaultRouter

from retail_chain.apps import RetailChainConfig
from retail_chain.views import (FactoryViewSet, NodeViewSet, ProductViewSet,
                                SearchByCountryView, SearchNodeByCountryView, SearchFactoryByCountryView)

app_name = RetailChainConfig.name

router1 = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()
router1.register(r"product", ProductViewSet, basename="product")
router2.register(r"node", NodeViewSet, basename="node")
router3.register(r"factory", FactoryViewSet, basename="factory")

urlpatterns = [
    path('node/search_by_country/', SearchNodeByCountryView.as_view(), name='search_node_by_country'),
    path('factory/search_by_country/', SearchFactoryByCountryView.as_view(), name='search_factory_by_country'),
] + router1.urls + router2.urls + router3.urls
