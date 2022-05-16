from pprint import pprint

from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from callup.engine import *
from callup.models import *
from callup.serializers import StationTypeSerializer, MatrixSerializer, UserStatusSerializer
from xpo_mgmt_api.engine import *


class LoginStation(APIView):
    def post(self, request):
        """
        Login on workstation. If any issues are active - reject request.

        Validate parameter. Check if station exists. Check if user or station has any active sessions,
        if so: close them. Validate if there's already active session on with user and requested station.

        :param station: string with station scanned from QR codes
        """
        station = request.POST.get('station')

        # CHECK IF REQUIRED PARAMETER EXISTS
        if not station:
            return Response(data={'detail': 'Missing parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        # CHECK STATION LENGTH
        if len(station) != 8:
            return Response(data={'detail': 'Wrong parameter value.'}, status=status.HTTP_400_BAD_REQUEST)

        station_type = station[:4].strip()
        line = station[4].strip()
        number = station[5:].strip()

        station = Station.objects.filter(Q(type__name=station_type) & Q(line=line) & Q(number=number)).first()

        # CHECK IF STATION EXISTS
        if not station:
            return Response(data={'detail': 'Station not found.'}, status=status.HTTP_404_NOT_FOUND)

        # CHECK IF USER HAS ACTIVE ISSUE
        user = get_user_from_token(request)
        current_user_issue = IssueLog.objects.filter(Q(user=user) & Q(closed__isnull=True)).first()
        if current_user_issue:
            return Response(data={'detail': 'User has ongoing issue open.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # CLOSE ANY OTHER SESSIONS OPENED ON REQUESTED STATION OR USER
        sessions = OccupationLog.objects.filter((Q(station=station) | Q(user=user)) & Q(logout__isnull=True))
        user_station_active_session = sessions.filter(Q(station=station) & Q(user=user)).first()
        sessions = sessions.exclude(Q(station=station) & Q(user=user))
        sessions.update(logout=timezone.now(), logout_type='F')

        # LOG IN ON STATION
        if not user_station_active_session:
            login_user_on_station(user, station)
        return Response(data=None, status=status.HTTP_200_OK)


class LogoutStation(APIView):
    def get(self, request):
        """
        Logout user from workstation.

        Administratively close all active issues. Logout user from all workstations.
        """
        user = get_user_from_token(request)

        # CLOSE ALL ACTIVE ISSUES
        issues = IssueLog.objects.filter(Q(user=user) & Q(closed__isnull=True))
        if issues:
            close_user_issue(issues=issues, comment="CLOSED ON USER STATION LOGOUT", supervisor=user)

        # LOGOUT FROM ALL STATIONS
        logout_user_from_station(user)

        return Response(data=None, status=status.HTTP_200_OK)


class ReportStation(APIView):
    def get(self, request, station_type):
        """
        List all stations with logged users and their statuses.

        :return: List of all stations with active users.
        """

        # FIND STATION TYPE
        user = get_user_from_token(request)
        stations, response = get_station_type_by_name(station_type.upper())
        if not stations:
            return response

        # CHECK PERMISSIONS
        if not user.has_perm('callup.can_view_issue_report'):
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

        # ACTIVE LINES
        lines = Station.objects.filter(occupation_log_station__logout__isnull=True, type=stations) \
            .values('type__name', 'line').distinct().order_by('line')
        return Response(data=MatrixSerializer(lines, many=True).data, status=status.HTTP_200_OK)


class ReportLine(APIView):
    def get(self, request, station_type, line):
        """
        List all stations with logged users and their statuses.

        :return: List of all stations with active users.
        """

        # FIND STATION TYPE
        user = get_user_from_token(request)
        stations, response = get_station_type_by_name(station_type.upper())
        if not stations:
            return response

        # FIND LINE
        line, response = get_line_by_station_type(stations, line)
        if not line:
            return response

        # CHECK PERMISSIONS
        if not user.has_perm('callup.can_view_issue_report'):
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

        # ACTIVE LINES
        active_users = OccupationLog.objects.filter(logout__isnull=True, station__type=stations, station__line=line)

        return Response(data=sort_user_status_serializer(UserStatusSerializer(active_users, many=True).data),
                        status=status.HTTP_200_OK)


class ReportStationType(APIView):
    def get(self, request):

        # CHECK PERMISSIONS
        user = get_user_from_token(request)
        if not user.has_perm('callup.can_view_issue_report'):
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

        station_types = StationType.objects.all()
        return Response(data=StationTypeSerializer(station_types, many=True).data, status=status.HTTP_200_OK)
