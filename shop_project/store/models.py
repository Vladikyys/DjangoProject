from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Genre, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', max_length=150)
    price = models.IntegerField('Цена', default=0)
    availability = models.BooleanField('Наличие', default=True)
    quantity = models.IntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name='Принято к заказу', default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return "{}".format(self.user)


class CartItem(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price_sum = models.PositiveIntegerField('Общая сумма', default=0)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.price_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.cart)


class Order(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    accepted = models.BooleanField('Заказ выполнен', default=False)
    date = models.DateTimeField("Дата", default=timezone.now())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "{}".format(self.cart)