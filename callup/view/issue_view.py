from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from callup.engine import *
from callup.models import *
from callup.serializers import IssueTypeSerializer
from xpo_mgmt_api.engine import *


class OpenIssue(APIView):
    def get(self, request):
        """
        Returns list of available issues on user's station type.

        Check if user is logged in on station.
        :return: list of available issues on user's station type.
        """
        user = get_user_from_token(request)

        # CHECK IF USER IS LOGGED ON WORKSTATION
        station = get_user_active_station(user).first().station
        if not station:
            return Response(data={'detail': 'User not logged in on workstation.'},
                            status=status.HTTP_400_BAD_REQUEST)

        issue_types = IssueType.objects.filter(station_type=station.type)

        return Response(data=IssueTypeSerializer(issue_types, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Opens issue.

        :param issue_type_id: issue chosen by user
        """
        # CHECK IF PARAMETER WAS GIVEN
        issue_type_id = request.POST.get('issue_type_id')
        if not issue_type_id:
            return Response(data={'detail': 'Missing parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        # CHECK IF ISSUE WITH GIVEN ID EXISTS
        requested_issue = IssueType.objects.filter(pk=issue_type_id).first()
        if not requested_issue:
            return Response(data={'detail': 'Issue with requested id not found.'}, status=status.HTTP_404_NOT_FOUND)

        # CHECK IF USER IS LOGGED ON WORKSTATION
        user = get_user_from_token(request)
        station = get_user_active_station(user).first().station
        if not station:
            return Response(data={'detail': 'User not logged in on workstation.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # CHECK IF USER HAS ANY ACTIVE ISSUES
        active_issue = get_user_active_issue(user)
        if active_issue:
            return Response(data={'detail': 'User has already active issue.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # CHECK IF GIVEN ID IS ALLOWED FOR USER'S ACTIVE STATION TYPE
        if requested_issue.station_type != station.type:
            return Response(data={'detail': 'Requested issue is not allowed on this station type.'},
                            status=status.HTTP_400_BAD_REQUEST)

        open_user_issue(user, station, requested_issue)
        return Response(data=None, status=status.HTTP_200_OK)


class ResolveIssue(APIView):
    def get(self, request):
        """
        Resolve issue on user's request.
        """
        user = get_user_from_token(request)
        issue = get_user_active_issue(user)
        if not issue:
            return Response(data={'detail': 'User does not have any active sessions.'},
                            status=status.HTTP_404_NOT_FOUND)
        close_user_issue(issue, "CLOSED ON USER\'S REQUEST", supervisor=user)
        return Response(data=None, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Resolve issue on supervisor's request
        :param username: supervisor's username
        :param password: supervisor's password
        :param comment: resolution comment
        """
        # CHECK IF SUPERVISOR PASSWORD, NAME AND COMMENT WERE GIVEN
        sv_username = request.POST.get('username')
        sv_password = request.POST.get('password')
        comment = request.POST.get('comment')
        if not sv_username or not sv_password or not comment:
            return Response(data={'detail': 'Missing one of parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        # CHECK IF ISSUE IS ACTIVE
        user = get_user_from_token(request)
        issue = get_user_active_issue(user)
        if not issue:
            return Response(data={'detail': 'User does not have any active sessions.'},
                            status=status.HTTP_404_NOT_FOUND)
        # CHECK IF SUPERVISOR IS AUTHENTICATED
        supervisor = authenticate(None, username=sv_username, password=sv_password)
        if not supervisor:
            return Response(data={'detail': 'Supervisor is not authenticated.'},
                            status=status.HTTP_403_FORBIDDEN)

        # CHECK IF SUPERVISOR HAS SUFFICIENT PERMISSIONS
        if not supervisor.has_perm('callup.can_view_issue_report'):
            return Response(data={'detail': 'Supervisor not authorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        # CHECK IF COMMENT IS LONGER THAN 10 CHARACTERS
        if len(comment) < 10:
            return Response(data={'detail': 'Comment must have at least 10 characters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        close_user_issue(issue, comment.strip('\n'), supervisor)
        return Response(data=None, status=status.HTTP_200_OK)


class ReportIssue(APIView):
    def get(self, request):
        """
        Get report of all issues.

        :param start: start datetime
        :param end: closed datetime
        :param user: requestor
        :param supervisor: solver
        :param station_type: type of station
        :return: List of issues.
        """
        user = get_user_from_token(request)
        # CHECK PERMISSIONS
        if not user.has_perm('callup.can_view_issue_report'):
            return Response(data={'detail': 'User not authorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        start = request.query_params.get('start')
        end = request.query_params.get('end')
        requestor = request.query_params.get('user')
        supervisor = request.query_params.get('supervisor')
        station_type = request.query_params.get('station_type')
        qs = IssueLog.objects.all()
        if start and len(start) == 12:
            start = get_datetime(start)
            if start:
                qs = qs.filter(created__gte=start)
        if end and len(end) == 12:
            end = get_datetime(end)
            if end:
                qs = qs.filter(created__lte=end)
        if requestor:
            qs = qs.filter(user__username=requestor)

        if supervisor:
            qs = qs.filter(supervisor__username=supervisor)

        if station_type:
            qs = qs.filter(station__type__name=station_type)

        data = list()
        for issue in qs:
            data.append({
                'created': issue.created,
                'closed': issue.closed if issue.closed else None,
                'user': issue.user.username,
                'station': issue.station.type.name + issue.station.line + issue.station.number,
                'supervisor': issue.supervisor.username if issue.supervisor else None,
                'issue_Type': issue.issue_type.issue_type,
                'comment': issue.comment if issue.comment else None
            })

        return Response(data=data, status=status.HTTP_200_OK)
