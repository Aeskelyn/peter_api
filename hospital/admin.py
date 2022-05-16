from django.contrib import admin
from django.utils.safestring import mark_safe

from hospital.models import *


class Locations(admin.ModelAdmin):
    list_display = ('location', 'location_type')
    list_filter = ('location_type',)
    search_fields = ('location',)


class OrderLines(admin.TabularInline):
    model = OrderLine
    fields = ('sku', 'coo', 'po', 'season', 'added', 'added_by', 'item_assigned')
    readonly_fields = ('added', 'added_by', 'item_assigned')

    def item_assigned(self, obj):
        return True if obj.taken_to.first().sku else False

    item_assigned.boolean = True


class OrderHeaders(admin.ModelAdmin):
    inlines = [OrderLines]
    list_display = ('order_number', 'location', 'wave', 'pick_sequence', 'closed', 'order_display')
    search_fields = ('order_number', 'location', 'wave')
    list_filter = ('pick_sequence', 'closed')

    @mark_safe
    def order_display(self, obj):
        return '<br>'.join([ol.sku if ol.taken_to.first() else '<b>' + ol.sku + '</b>' for ol in obj.orders.all()])

    order_display.short_description = 'SKUs'


class Items(admin.ModelAdmin):
    list_display = ('sku', 'coo', 'po', 'season', 'added', 'added_by', 'taken', 'taken_by', 'taken_to', 'location')
    list_filter = ('taken',)
    search_fields = ('sku', 'location__location')


admin.site.register(Location, Locations)
admin.site.register(OrderHeader, OrderHeaders)
admin.site.register(Item, Items)
