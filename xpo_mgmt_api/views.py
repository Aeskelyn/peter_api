from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from xpo_mgmt_api.engine import *
from callup.engine import *


class Logout(APIView):
    def get(self, request):
        type = request.query_params.get('type')
        if not type:
            return Response(data={'detail': 'Missing parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        if type.upper() not in ('F', 'M'):
            return Response(data={'detail': 'Wrong parameter value.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_from_token(request)
        issues = get_user_active_issue(user)
        if issues:
            close_user_issue(issues, "CLOSED ON USER\'S LOGOUT")
        logout_user_from_station(user, type.upper())
        return Response(data=None, status=status.HTTP_200_OK)
