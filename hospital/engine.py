import re

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from hospital.models import Item, OrderHeader, OrderLine, Location
from django.utils import timezone


# ORDER MANAGEMENT
def add_order_to_location(user, order, location):
    order.location = location
    order.location_by = user
    order.location_at = timezone.now()
    order.save()


def remove_order_from_location(user, item):
    item.location = None
    item.location_by = user
    item.location_at = timezone.now()
    item.save()


# ITEM MANAGEMENT
def add_it69_to_location(user, it69, location):
    sku, coo, po, season = decode_it69(it69)
    it69 = Item(sku=sku, coo=coo, po=po, season=season, added_by=user, location=location)
    ol = OrderLine.objects.filter(Q(sku=sku) & Q(taken_to__sku__isnull=True) & Q(order__closed__isnull=True)).order_by(
        'added').first()
    if ol:
        it69.taken_to = ol
        it69.taken_by = user
        it69.taken = timezone.now()
    it69.save()


def remove_it69_from_location(user, it69, location):
    sku, coo, po, season = decode_it69(it69)
    i = Item.objects.filter(
        Q(sku=sku) & Q(coo=coo) & Q(po=po) & Q(season=season) & Q(location=location) & Q(taken__isnull=True)).order_by(
        'added').first()
    if not i:
        return True
    i.taken = timezone.now()
    i.taken_by = user
    i.save()
    return False


def decode_it69(item):
    sku = item[2:15]
    coo = item[27:29]
    po = item[21:27]
    season = item[15:21]
    return sku, coo, po, season


def is_valid_it69(it69):
    it = it69
    response = None
    if not (len(it69) == 29 and re.match(r'[0-9]{27}[A-Za-z]{2}', it69)):
        it = None
        response = Response(data={'detail': 'Not a valid IT69.'}, status=status.HTTP_400_BAD_REQUEST)
    return it, response


def is_valid_order_number(order_number):
    order = None
    response = None
    if len(order_number) == 14 and re.match(r'[A-Z]{2}[a-z][0-9]{11}', order_number):
        order = order_number[2:]
    elif len(order_number) == 12 and re.match(r'[a-z][0-9]{11}', order_number):
        order = order_number
    else:
        response = Response(data={'detail': 'Not a valid order number.'}, status=status.HTTP_400_BAD_REQUEST)
    return order, response


def find_order_header_by_order_number(order_number):
    order = OrderHeader.objects.filter(order_number=order_number).first()
    response = None
    if not order:
        response = Response(data={'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
    return order, response


def find_location_object_by_location(location):
    location_object = Location.objects.filter(location=location).first()
    response = None
    if not location_object:
        response = Response(data={'detail': 'Location does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    return location_object, response


def is_closed_order(order):
    is_closed = False
    response = None
    if order.closed:
        is_closed = True
        response = Response(data={'detail': 'Order already closed.'}, status=status.HTTP_400_BAD_REQUEST)
    return is_closed, response


def close_order(order, user):
    order.closed = timezone.now()
    order.closed_by = user
    order.save()
