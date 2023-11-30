from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=200
    )
    description = models.TextField(
        max_length=1000
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=3,
        default="usd"
    )


class Order(models.Model):
    items = models.ManyToManyField(
        Item,
        related_name="orders"
    )
    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True
    )
    tax = models.ForeignKey(
        'Tax',
        on_delete=models.SET_NULL,
        null=True
    )


class Discount(models.Model):
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )


class Tax(models.Model):
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
