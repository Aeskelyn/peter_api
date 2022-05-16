from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from callup.engine import sort_user_status_serializer
from callup.models import IssueType, StationType, Station, IssueLog, Score, OccupationLog


class IssueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueType
        fields = ['id', 'issue_type']
        read_only_fields = ['id', 'issue_type']


class StationTypeSerializer(serializers.ModelSerializer):
    lines = SerializerMethodField()

    class Meta:
        model = StationType
        fields = ['name', 'lines']
        read_only_fields = ['name']

    @staticmethod
    def get_lines(instance):
        lines = Station.objects.filter(type=instance).values_list('line', flat=True).distinct().order_by('line')
        return lines



class StationSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = Station
        fields = ['type', 'line', 'number']


class UserStatusSerializer(serializers.ModelSerializer):
    location = StationSerializer(source='station', read_only=True)
    scores = SerializerMethodField()
    issue = SerializerMethodField()
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = OccupationLog
        fields = ['user', 'location', 'scores', 'issue']

    @staticmethod
    def get_scores(instance):
        scores = Score.objects.filter(user=instance.user.username, station_type=instance.station.type.name)
        return ScoreSerializer(scores.first()).data

    @staticmethod
    def get_issue(instance):
        issues = IssueLog.objects.filter(closed__isnull=True, user=instance.user)
        return IssueSerializer(issues.first()).data


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['previous', 'current', 'estimated']


class IssueSerializer(serializers.ModelSerializer):
    issue_type = serializers.CharField(source='issue_type.issue_type')

    class Meta:
        model = IssueLog
        fields = ['created', 'issue_type']


class MatrixSerializer(serializers.Serializer):
    line = serializers.CharField()
    stations = serializers.SerializerMethodField()

    class Meta:
        fields = ['line', 'stations']

    @staticmethod
    def get_stations(instance):
        stations = OccupationLog.objects.filter(logout__isnull=True,
                                                station__type__name=instance['type__name'],
                                                station__line=instance['line'])
        data = UserStatusSerializer(stations, many=True).data
        data_sorted = sort_user_status_serializer(data)
        return data_sorted
