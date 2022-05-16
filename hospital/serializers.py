from django.db.models import Q
from rest_framework import serializers

from hospital.models import Item, OrderHeader, OrderLine, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location']


class ItemSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='location.location', read_only=True)

    class Meta:
        model = Item
        fields = ['sku', 'location']


class OrderLineSerializer(serializers.ModelSerializer):
    found_at = serializers.SerializerMethodField()

    class Meta:
        model = OrderLine
        fields = ['sku', 'found_at']

    @staticmethod
    def get_found_at(instance):
        location = None
        if instance.taken_to.exists():
            location = instance.taken_to.first().location.location
        return location


class OrderSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    order_lines = OrderLineSerializer(source='orders', read_only=True, many=True)
    location = serializers.CharField(source='location.location', read_only=True)
    location_by = serializers.CharField(source='location_by.username', read_only=True)

    class Meta:
        model = OrderHeader
        fields = ['order_number', 'created', 'closed', 'location', 'location_at', 'location_by', 'order_lines']

    @staticmethod
    def get_created(instance):
        order_lines = OrderLine.objects.filter(order=instance)
        oldest_line = order_lines.order_by('added').first()
        dt = oldest_line.added
        return dt.astimezone().isoformat()


class ItemStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['sku', 'added']


class LocationStockSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    oldest = serializers.SerializerMethodField()
    newest = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['location', 'items', 'newest', 'oldest']

    @staticmethod
    def get_items(instance):
        items = Item.objects.filter(Q(location__location=instance.location) & Q(taken__isnull=True))
        return ItemStockSerializer(items, many=True).data

    @staticmethod
    def get_oldest(instance):
        items = Item.objects.filter(Q(location__location=instance.location) & Q(taken__isnull=True))
        oldest = items.order_by('added').first().added
        return oldest.astimezone().isoformat()

    @staticmethod
    def get_newest(instance):
        items = Item.objects.filter(Q(location__location=instance.location) & Q(taken__isnull=True))
        newest = items.order_by('-added').first().added
        return newest.astimezone().isoformat()
