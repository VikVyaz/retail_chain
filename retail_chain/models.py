from django.db import models


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

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class SupplyChainNode(models.Model):
    """Модель звена цепи поставок"""

    CHAIN_ROLE = [
        ('factory', 'Завод'),
        ('retail_network', 'Розничная сеть'),
        ('sole_proprietor', 'Индивидуальный предприниматель'),
    ]

    title = models.CharField(
        max_length=50,
        verbose_name='Название звена цепи поставки',
        help_text='Название звена цепи поставки'
    )
    supply_chain_role = models.CharField(
        choices=CHAIN_ROLE,
        max_length=50,
        verbose_name='Тип звена цепи поставок',
        help_text='Варианты:\n'
                  'factory - завод(supplier будет отсутствовать),\n'
                  'retail_network - розничная сеть,\n'
                  'sole_proprietor - индивидуальный предприниматель.'
    )
    email = models.EmailField(
        verbose_name='Email звена цепи поставок',
        help_text='Email звена цепи поставок'
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
    products = models.ManyToManyField(
        Product,
        related_name='supply_nodes',
        verbose_name='Продукты, которые были получены от поставщика',
        help_text='id продуктов'
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='node_supplier',
        null=True,
        blank=True,
        verbose_name='Поставщик',
        help_text='id поставщика. Если supply_chain_role "factory" - supplier автоматически null'
    )
    debt = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        verbose_name='Долг перед поставщиком',
        help_text='Формат: "12.34". Обновление недоступно через API.'
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания звена цепи поставок',
        help_text=' Выставляется автоматически при создании.'
    )
    chain_level = models.IntegerField(
        default=0,
        verbose_name='Уровень в иерархии поставок',
        help_text='Уровень в иерархии поставок. Количество поставщиков от завода.'
    )

    class Meta:
        verbose_name = 'Звено цепи поставок'
        verbose_name_plural = 'Звенья цепи поставок'

    @property
    def contacts(self):
        return {
            'email': self.email,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number
        }
