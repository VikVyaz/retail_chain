from retail_chain.apps import RetailChainConfig
from rest_framework.routers import DefaultRouter

from retail_chain.views import ProductViewSet, NodeViewSet

app_name = RetailChainConfig.name

router1 = DefaultRouter()
router2 = DefaultRouter()
router1.register(r"product", ProductViewSet, basename="product")
router2.register(r"node", NodeViewSet, basename="node")

urlpatterns = [

] + router1.urls + router2.urls
