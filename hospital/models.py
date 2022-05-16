from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    location_choices = (
        ('ORDER', 'Order'),
        ('ITEM', 'Item'),
    )
    location_model =(
        ('FPS', 'Fps'),
        ('MIX', 'Mix'),
    )
    location = models.CharField(max_length=8, unique=True)
    location_type = models.CharField(max_length=5, choices=location_choices)
    location_modelchoice = models.CharField(max_length=3, choices=location_model,default='FPS')

    def __str__(self):
        return self.location


class OrderHeader(models.Model):
    class Meta:
        verbose_name = 'Order'
    order_number = models.CharField(max_length=12, unique=True)
    wave = models.CharField(max_length=13, blank=True)
    pick_sequence = models.CharField(max_length=13, blank=True)
    closed = models.DateTimeField(blank=True, null=True)
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='closed_by')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='order_location')
    location_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocated_by')
    location_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.order_number


class OrderLine(models.Model):
    sku = models.CharField(max_length=13)
    coo = models.CharField(max_length=2, blank=True)
    po = models.CharField(max_length=6, blank=True)
    season = models.CharField(max_length=6, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderHeader, on_delete=models.SET_NULL, null=True, related_name='orders')

    def __str__(self):
        return self.order.order_number + ' | ' + self.sku


class Item(models.Model):
    sku = models.CharField(max_length=13)
    coo = models.CharField(max_length=2)
    po = models.CharField(max_length=6)
    season = models.CharField(max_length=6)
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_by')
    taken = models.DateTimeField(blank=True, null=True)
    taken_to = models.ForeignKey(OrderLine, blank=True, on_delete=models.SET_NULL, null=True, related_name='taken_to')
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='taken_by')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='item_location')

    def __str__(self):
        return self.sku
