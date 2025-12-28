import pytest
from rest_framework.test import APIClient

from users.models import User
from .models import SupplyChainNode, Product

class TestNodeAPI:

    @pytest.fixture(scope='class')
    def setup_method(self):
        self.client = APIClient()
        self.active_user = User.objects.create_user(
            username='test_active',
            password='1234'
        )
        self.not_active_user = User.objects.create_user(
            username='test_not_active',
            password='1234'
        )
        self.product = Product.objects.create(
            title='test_prod',
            model='v1.0',
            release_date='2025-12-23',
            price='12.34'
        )
        self.factory_node = SupplyChainNode.objects.create(
            title='test_factory',
            supply_chain_role='factory',
            email='test@test.com',
            country='Spain',
            city='test_city',
            street='test_street',
            house_number='14b',
            products=[self.product],
            supplier=None,
            debt='12.34'
        )
        self.not_factory_node_1 = SupplyChainNode.objects.create(
            title='test_not_factory_1',
            supply_chain_role='retail_network',
            email='test@test.com',
            country='France',
            city='test_city',
            street='test_street',
            house_number='14b',
            products=[self.product],
            supplier=None,
            debt='12.34'
        )
        self.not_factory_node_2 = SupplyChainNode.objects.create(
            title='test_not_factory_2',
            supply_chain_role='sole_proprietor',
            email='test@test.com',
            country='Germany',
            city='test_city',
            street='test_street',
            house_number='14b',
            products=[self.product],
            supplier=None,
            debt='12.34'
        )


