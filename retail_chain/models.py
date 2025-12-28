from django.db import models


class Factory(models.Model):
    """Модель для Завода"""

    title = models.CharField(
        max_length=50,
        verbose_name='Название звена цепи поставки',
        help_text='Название звена цепи поставки'
    )
    email = models.EmailField(
        verbose_name='Email завода',
        help_text='Email завода'
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Страна, где находится звено цепи поставок',
        help_text='Страна, где находится звено цепи поставок'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город, где находится звено цепи поставок',
        help_text='Город, где находится звено цепи поставок'
    )
    street = models.CharField(
        max_length=100,
        verbose_name='Улица, на которой находится звено цепи поставок',
        help_text='Улица, на которой находится звено цепи поставок'
    )
    house_number = models.CharField(
        max_length=10,
        verbose_name='Номер дома, на которой находится звено цепи поставок',
        help_text='Номер дома, на которой находится звено цепи поставок'
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания звена цепи поставок',
        help_text=' Выставляется автоматически при создании.'
    )

    class Meta:
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'

    @property
    def contacts(self):
        return {
            'title': self.title,
            'email': self.email,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number
        }

    @property
    def supply_chain_role(self):
        return 'factory'

    @property
    def chain_level(self):
        return 0


class Product(models.Model):
    """Модель продукта для реализации"""

    title = models.CharField(
        max_length=50,
        verbose_name='Название продукта',
        help_text='Название продукта'
    )
    model = models.CharField(
        max_length=100,
        verbose_name='Модель продукта',
        help_text='Модель продукта'
    )
    release_date = models.DateField(
        verbose_name='Дата выхода продукта на рынок',
        help_text='Формат: "ГГГГ-ММ-ДД"'
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Цена продукта',
        help_text='Формат: "12.34"'
    )
    produced_by = models.ForeignKey(
        Factory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produced_products',
        verbose_name='Завод, который произвел этот продукт',
        help_text='Завод, который произвел этот продукт'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class SupplyChainNode(models.Model):
    """Модель звена цепи поставок"""

    CHAIN_ROLE = [
        ('retail_network', 'Розничная сеть'),
        ('sole_proprietor', 'Индивидуальный предприниматель'),
    ]
    SUPPLIER_TYPE = [
        ('factory', 'Завод'),
        ('another_node', 'Другие звенья цепи поставок')
    ]

    title = models.CharField(
        max_length=50,
        verbose_name='Название звена цепи поставки',
        help_text='Название звена цепи поставки'
    )
    email = models.EmailField(
        verbose_name='Email завода',
        help_text='Email завода'
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Страна, где находится звено цепи поставок',
        help_text='Страна, где находится звено цепи поставок'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город, где находится звено цепи поставок',
        help_text='Город, где находится звено цепи поставок'
    )
    street = models.CharField(
        max_length=100,
        verbose_name='Улица, на которой находится звено цепи поставок',
        help_text='Улица, на которой находится звено цепи поставок'
    )
    house_number = models.CharField(
        max_length=10,
        verbose_name='Номер дома, на которой находится звено цепи поставок',
        help_text='Номер дома, на которой находится звено цепи поставок'
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания звена цепи поставок',
        help_text=' Выставляется автоматически при создании.'
    )
    supply_chain_role = models.CharField(
        choices=CHAIN_ROLE,
        max_length=50,
        verbose_name='Тип звена цепи поставок',
        help_text='Варианты:\n'
                  'retail_network - розничная сеть,\n'
                  'sole_proprietor - индивидуальный предприниматель.'
    )
    products = models.ManyToManyField(
        Product,
        related_name='supply_nodes',
        verbose_name='Продукты, которые были получены от поставщика',
        help_text='id продуктов. Формат: [1, 2, 3,...].'
    )
    supplier_type = models.CharField(
        choices=SUPPLIER_TYPE,
        verbose_name='Поставщик',
        help_text='Тип поставщика.\n'
                  'Варианты:\n'
                  '"factory" - завод,\n'
                  '"another_node" - другие звенья цепи поставок (розничная сеть или ИП).'
    )
    supplier_id = models.PositiveIntegerField(
        verbose_name='Id поставщика',
        help_text='Id поставщика'
    )
    debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name='Долг перед поставщиком',
        help_text='Формат: "12.34". Обновление недоступно через API.'
    )

    class Meta:
        verbose_name = 'Звено цепи поставок'
        verbose_name_plural = 'Звенья цепи поставок'

    @property
    def contacts(self):
        return {
            'title': self.title,
            'email': self.email,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number
        }

    @property
    def _supplier_obj(self):
        if self.supplier_type == 'factory':
            return Factory.objects.filter(id=self.supplier_id).first()
        return SupplyChainNode.objects.filter(id=self.supplier_id).first()

    @property
    def chain_level(self):
        return self._supplier_obj.chain_level + 1
