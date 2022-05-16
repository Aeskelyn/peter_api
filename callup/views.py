from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from callup.engine import *
from callup.models import *
from xpo_mgmt_api.engine import *


class Status(APIView):
    """
    Returns overall user status.
    """
    def get(self, request):
        content = {
            'station': None,
            'score': None,
            'issue': None
        }
        user = get_user_from_token(request)
        issue = IssueLog.objects.filter(Q(user=user) & Q(closed__isnull=True)).first()
        occupation = OccupationLog.objects.filter(Q(user=user) & Q(logout__isnull=True)).first()

        if occupation:
            content['station'] = {
                'type': {
                    'name': occupation.station.type.name,
                    'is_measurable': occupation.station.type.is_measurable
                },
                'line': occupation.station.line,
                'number': occupation.station.number
            }
            if occupation.station.type.is_measurable:
                score = Score.objects.filter(
                    Q(user=user.username) & Q(station_type=occupation.station.type.name))
                if score.count() > 0:
                    content['score'] = {
                        'current': score.aggregate(Sum('current'))['current__sum'],
                        'previous': score.aggregate(Sum('previous'))['previous__sum'],
                        'estimated': score.aggregate(Sum('estimated'))['estimated__sum']
                    }
        if issue:
            content['issue'] = {
                'id': issue.id,
                'issue_type': issue.issue_type.issue_type,
                'created': issue.created
            }
        return Response(data=content, status=status.HTTP_200_OK)
