# from pprint import pprint
#
# from django.test import TestCase
# from callup.view.station_view import *
# from callup.view.issue_view import *
#
#
# class StationTestCase(TestCase):
#     request = {
#         'META': dict(),
#         'POST': dict()
#     }
#
#     def setUp(self):
#         StationType.objects.create(name='RET', is_measurable=True)
#         StationType.objects.create(name='VAS', is_measurable=False)
#         StationType.objects.create(name='PACK', is_measurable=True)
#
#         Station.objects.create(type=StationType.objects.get(name='RET'), line='A', number='001')
#         Station.objects.create(type=StationType.objects.get(name='RET'), line='B', number='002')
#         Station.objects.create(type=StationType.objects.get(name='VAS'), line='.', number='001')
#         Station.objects.create(type=StationType.objects.get(name='VAS'), line='.', number='002')
#         Station.objects.create(type=StationType.objects.get(name='PACK'), line='1', number='001')
#         Station.objects.create(type=StationType.objects.get(name='PACK'), line='2', number='002')
#
#         User.objects.create_user(username='test', email='test@test.com', password='22test22')
#         User.objects.create_user(username='test2', email='test@test.com', password='22test22')
#
#     def test_check_station_type(self):
#         self.assertEqual(StationType.objects.all().count(), 3)
#
#     def test_check_station_number(self):
#         self.assertEqual(Station.objects.all().count(), 6)
#
#     def test_user_count(self):
#         self.assertEqual(User.objects.all().count(), 2)
#
#     def test_login_on_station(self):
#         user = User.objects.get(username='test')
#         token = Token.objects.create(user=user)
#         self.request['META']['HTTP_AUTHORIZATION'] = 'Token ' + str(token)
#         self.request['POST']['station'] = 'RET A001'
#         pprint(self.request)
#         LoginStation.post(None, request=self.request)
#         self.assertEqual(OccupationLog.objects.filter(station__issuelog__closed__isnull=True).count(), 1)
#
#     def test_login_on_already_occupied_station(self):
#         station = Station.objects.get(type__name='RET', line='A', number='001')
#         user2 = User.objects.get(username='test2')
#         user = User.objects.get(username='test')
#         login_user_on_station(user, station)
#         print(OccupationLog.objects.all())
#         login_user_on_station(user2, station)
#         self.assertEqual(OccupationLog.objects.filter(station__issuelog__closed__isnull=True).count(), 1)
