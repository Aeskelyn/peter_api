import datetime, pytz
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# AUTH

def get_user_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION').split()[1]
    username = Token.objects.get(key=token).user
    return User.objects.get(username=username)


# OPS FUNCTIONS

def get_datetime(dt):
    return datetime.datetime(int(dt[0:4]), int(dt[4:6]), int(dt[6:8]), int(dt[8:10]),
                             int(dt[10:12]), 0, 0, pytz.utc)
