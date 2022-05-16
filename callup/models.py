from django.contrib.auth.models import User
from django.db import models


class StationType(models.Model):
    name = models.CharField(max_length=4, unique=True)
    is_measurable = models.BooleanField(default=False, null=False, blank=False)
    is_manualhospital= models.BooleanField(default=False, null=False, blank=False)
    
    def __str__(self):
        return self.name


class Station(models.Model):
    type = models.ForeignKey(StationType, on_delete=models.SET_NULL, null=True)
    line = models.CharField(max_length=1)
    number = models.CharField(max_length=3)
     
    def __str__(self):
        return self.type.name + self.line + self.number


class OccupationLog(models.Model):
    class Meta:
        permissions = (
            ('can_view_station_report', 'Can view station report'),
        )
    LOGOUT_TYPE = (
        ('M', 'MANUAL'),
        ('F', 'FORCED'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, related_name='occupation_log_station')
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(null=True, blank=True, db_index=True)
    logout_type = models.CharField(max_length=1, choices=LOGOUT_TYPE, blank=True, null=True)


class IssueType(models.Model):
    station_type = models.ForeignKey(StationType, on_delete=models.SET_NULL, null=True, related_name='issues')
    issue_type = models.CharField(max_length=50)

    def __str__(self):
        return self.issue_type


class IssueLog(models.Model):
    class Meta:
        permissions = (
            ('can_resolve_issue', 'Can resolve issue'),
            ('can_view_issue_report', 'Can view issue report'),
        )
    created = models.DateTimeField(auto_now_add=True)
    closed = models.DateTimeField(null=True, blank=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issue_user')
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='issue_supervisor')
    issue_type = models.ForeignKey(IssueType, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)


class Score(models.Model):
    user = models.CharField(max_length=50)
    station_type = models.CharField(max_length=4)
    previous = models.IntegerField()
    current = models.IntegerField()
    estimated = models.IntegerField()
