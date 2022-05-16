from rest_framework.views import APIView
from rest_framework import filters
from hospital.engine import *
from hospital.serializers import *
from xpo_mgmt_api.engine import *
from hospital.models import *


class ItemList(APIView):
    def get(self, request):
        items = Item.objects.filter(taken__isnull=True)
        return Response(data=ItemSerializer(items, many=True).data, status=status.HTTP_200_OK)


class ItemDetail(APIView):
    def get(self, request, sku):
        items = Item.objects.filter(taken__isnull=True, sku=sku)
        return Response(data=ItemSerializer(items, many=True).data, status=status.HTTP_200_OK)


class Manage(APIView):
    def post(self, request):
        """
        Add or remove item/order from location
        :param item: string
        :param location: string
        :param action: {'PtAw': put away
                        'PkUp': pickup}
        """
        # GATHER DATA
        user = get_user_from_token(request)
        item = request.POST.get('item')
        location = request.POST.get('location')
        action = request.POST.get('action')
        item_is_order = False
        location_is_order = False

        # CHECK REQUIREMENT FIELDS
        if not item:
            return Response(data={'detail': 'Missing operation object.'}, status=status.HTTP_400_BAD_REQUEST)

        if not location:
            return Response(data={'detail': 'Missing location.'}, status=status.HTTP_400_BAD_REQUEST)

        if not action:
            return Response(data={'detail': 'Missing action.'}, status=status.HTTP_400_BAD_REQUEST)

        # IDENTIFY OBJECT
        it69, _ = is_valid_it69(item)
        order_number, _ = is_valid_order_number(item)
        if it69:
            # IT69, ex. 090369796007001201909146984CN
            pass
        elif order_number:
            # order with COO, ex. PLa21985778624, a21985778624
            item_is_order = True

            # IF ORDER CHECK IF EXISTS
            order, response = find_order_header_by_order_number(order_number)
            if not order:
                return response
        else:
            return Response(data={'detail': 'Not a valid item.'}, status=status.HTTP_400_BAD_REQUEST)

        # FIND LOCATION
        location, response = find_location_object_by_location(location)
        if not location:
            return response
        if location.location_type == 'ORDER':
            location_is_order = True

        # CHECK IF LOCATION TYPE MATCHES OBJECT TYPE
        if location_is_order != item_is_order:
            return Response(data={'detail': 'Wrong location type.'}, status=status.HTTP_400_BAD_REQUEST)

        # PERFORM ACTIONS
        if action == 'PtAw':
            if item_is_order:
                if order.location:
                    return Response(data={'detail': 'Order already allocated.'}, status=status.HTTP_400_BAD_REQUEST)
                add_order_to_location(user, order, location)
            else:
                add_it69_to_location(user, it69, location)
        elif action == 'PkUp':
            if item_is_order:
                if not order.location:
                    return Response(data={'detail': 'Order not allocated.'}, status=status.HTTP_400_BAD_REQUEST)
                remove_order_from_location(user, order)
            else:
                if remove_it69_from_location(user, it69, location):
                    return Response(data={'detail': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={'detail': 'Wrong action code.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=None, status=status.HTTP_200_OK)


class OrderList(APIView):
    def get(self, request):
        return Response(data=OrderSerializer(OrderHeader.objects.filter(closed__isnull=True), many=True).data,
                        status=status.HTTP_200_OK)

    def post(self, request):
        user = get_user_from_token(request)
        order = request.POST.get('order')
        sku = request.POST.get('sku')

        # CHECK IF ALL PARAMETERS EXISTS
        if not (order and sku):
            return Response(data={'detail': 'Missing parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        # CHECK IF PATTERNS MACHES:
        if not (re.match(r'[A-Z]{2}[a-z][0-9]{11}', order) or re.match(r'[a-z][0-9]{11}', order)):
            return Response(data={'detail': 'Wrong order number pattern.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r'[0-9]{13}', sku):
            return Response(data={'detail': 'Wrong SKU pattern.'}, status=status.HTTP_400_BAD_REQUEST)

        # ADD REQUEST
        # CHECK IF ORDER HEADER ALREADY EXISTS
        oh = OrderHeader.objects.filter(order_number=order).first()
        if not oh:
            oh = OrderHeader.objects.create(order_number=order)
        OrderLine.objects.create(order=oh, sku=sku, added_by=user)
        return Response(data=None, status=status.HTTP_200_OK)


class OrderDetail(APIView):
    def get(self, request, order):
        # CHECK IF VALID ORDER NUMBER
        ordr, response = is_valid_order_number(order)
        if not ordr:
            return response

        # CHECK IF ORDER EXISTS
        ordr, response = find_order_header_by_order_number(ordr)
        if not ordr:
            return response
        return Response(data=OrderSerializer(ordr).data, status=status.HTTP_200_OK)

    def post(self, request, order):
        # CHECK IF VALID ORDER NUMBER
        ordr, response = is_valid_order_number(order)
        if not ordr:
            return response

        # CHECK IF ORDER EXISTS
        ordr, response = find_order_header_by_order_number(ordr)
        if not ordr:
            return response

        # CHECK IF ORDER IS CLOSED
        is_closed, response = is_closed_order(ordr)
        if is_closed:
            return response

        # CLOSE ORDER
        user = get_user_from_token(request)
        close_order(ordr, user)
        return Response(data=None, status=status.HTTP_200_OK)


class Recovery(APIView):
    def get(self, request):
        pass


class LocationStock(APIView):
    def get(self, request):
        locations = Location.objects.filter(
            Q(item_location__sku__isnull=False) & Q(item_location__taken__isnull=True)).distinct()
        return Response(data=LocationStockSerializer(locations, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        user = get_user_from_token(request)
        location = request.POST.get('location')

        if not location:
            return Response(data={'detail': 'No location parameter provided'}, status=status.HTTP_400_BAD_REQUEST)

        location, response = find_location_object_by_location(location)
        if not location:
            return response

        order_on_location = OrderHeader.objects.filter(closed__isnull=True, location=location)
        items_on_location = Item.objects.filter(taken__isnull=True, location=location)

        objects = order_on_location.count() + items_on_location.count()

        if objects == 0:
            return Response(data={'detail': 'No objects found on location.'}, status=status.HTTP_404_NOT_FOUND)

        order_on_location.update(closed=timezone.now(), closed_by=user)
        items_on_location.update(taken=timezone.now(), taken_by=user)

        return Response(data=None, status=status.HTTP_200_OK)
