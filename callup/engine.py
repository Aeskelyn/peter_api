from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from callup.models import *


# STATION

def login_user_on_station(user, station):
    OccupationLog.objects.create(user=user, station=station)


def get_user_active_station(user):
    log = OccupationLog.objects.filter(Q(user=user) & Q(logout__isnull=True))
    if not log:
        return None
    return log


def logout_user_from_station(user, logout_type='M'):
    qs = OccupationLog.objects.filter(Q(user=user) & Q(logout__isnull=True))
    qs.update(logout=timezone.now(), logout_type=logout_type)


# ISSUES

def open_user_issue(user, station, issue_type):
    IssueLog.objects.create(user=user, station=station, issue_type=issue_type)


def get_user_active_issue(user):
    issue = IssueLog.objects.filter(Q(user=user) & Q(closed__isnull=True))

    if not issue:
        return None
    return issue


def close_user_issue(issues, comment, supervisor=None):
    if not supervisor:
        supervisor = User.objects.get(username='system')
    issues.update(comment=comment, supervisor=supervisor, closed=timezone.now())


def get_station_type_by_name(station_type):
    station = StationType.objects.filter(name=station_type).first()
    response = None
    if not station:
        response = Response(data={'detail': 'Station type not found.'}, status=status.HTTP_404_NOT_FOUND)
    return station, response


def get_line_by_station_type(station_type, line):
    station = Station.objects.filter(type=station_type, line=line).first()
    response = None
    if not station:
        response = Response(data={'detail': 'Line not found on selected station type.'},
                            status=status.HTTP_404_NOT_FOUND)
    return station.line, response


def sort_user_status_serializer(data):
    return sorted(data, key=lambda x: (
        x['issue']['created'] if 'created' in x['issue'] else '',
        x['scores']['estimated'] if x['scores']['estimated'] else 0))
