import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from .models import Factory, Product, SupplyChainNode


class TestNodeAPI:
    """Тесты"""

    def setup_method(self):
        self.client = APIClient()
        self.active_user = User.objects.create_user(
            username='test_active',
            email='email1@mail.com',
            password='1234'
        )
        self.not_active_user = User.objects.create_user(
            username='test_not_active',
            email='email2@mail.com',
            password='1234'
        )
        self.factory = Factory.objects.create(
            title='test_factory',
            email='test@test.com',
            country='Spain',
            city='test',
            street='test',
            house_number='test',
        )
        self.product = Product.objects.create(
            title='test_prod',
            model='v1.0',
            release_date='2025-12-23',
            price='12.34',
            produced_by=self.factory
        )
        self.node_by_factory = SupplyChainNode.objects.create(
            title='test_node_1',
            email='test@test.com',
            country='Germany',
            city='test',
            street='test',
            house_number='test',
            supply_chain_role='sole_proprietor',
            supplier_type='factory',
            supplier_id=self.factory.pk,
            debt='12.34'
        )
        self.node_by_factory.products.set([self.product])
        self.node_by_another = SupplyChainNode.objects.create(
            title='test_node_2',
            email='test@test.com',
            country='Germany',
            city='test',
            street='test',
            house_number='test',
            supply_chain_role='sole_proprietor',
            supplier_type='another_node',
            supplier_id=self.factory.pk,
            debt='12.34'
        )
        self.node_by_another.products.set([self.product])

        self.client.force_authenticate(user=self.active_user)

    @pytest.mark.django_db
    def test_1_models(self):
        assert self.factory.contacts == {
            'title': 'test_factory',
            'email': 'test@test.com',
            'country': 'Spain',
            'city': 'test',
            'street': 'test',
            'house_number': 'test'
        }
        assert self.factory.supply_chain_role == 'factory'
        assert self.factory.chain_level == 0

        assert self.node_by_factory.contacts == {
            'title': 'test_node_1',
            'email': 'test@test.com',
            'country': 'Germany',
            'city': 'test',
            'street': 'test',
            'house_number': 'test'
        }

        assert self.node_by_factory.supplier_type == self.factory.supply_chain_role

        assert self.node_by_factory.chain_level == 1
        assert self.node_by_another.chain_level == 2

    @pytest.mark.django_db
    def test_2_setup_created(self):
        assert User.objects.count() == 2
        assert Factory.objects.count() == 1
        assert Product.objects.count() == 1
        assert SupplyChainNode.objects.count() == 2

    @pytest.mark.django_db
    def test_3_factory(self):
        url = reverse('retail_chain:factory-list')
        input_data = {
            'title': '1',
            'email': '1@1.com',
            'country': '1',
            'city': '1',
            'street': '1',
            'house_number': '1',
        }

        response = self.client.post(url, input_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['title'] == '1'

    @pytest.mark.django_db
    def test_4_product(self):
        url = reverse('retail_chain:product-list')
        input_data = {
            'title': '1',
            'model': '1',
            'release_date': '2025-12-12',
            'price': '12.34'
        }

        response = self.client.post(url, input_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'produced_by': ['Такого завода-изготовителя не существует']}

        input_data['produced_by'] = self.factory.pk
        response = self.client.post(url, input_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['title'] == '1'
