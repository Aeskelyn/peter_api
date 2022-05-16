from django.contrib import admin
from django.utils.safestring import mark_safe

from callup.models import *


class OccupationLogs(admin.ModelAdmin):
    list_display = ('user', 'station', 'login', 'logout', 'logout_type',)
    list_filter = ('logout_type', 'logout')


class IssueLogs(admin.ModelAdmin):
    list_display = ('user', 'station', 'supervisor', 'created', 'closed', 'issue_type', 'comment')
    list_filter = ('created', 'closed')


class IssueTypes(admin.TabularInline):
    model = IssueType


class StationTypes(admin.ModelAdmin):
    inlines = [IssueTypes]
    list_display = ('name', 'issues_display', 'is_measurable')

    @mark_safe
    def issues_display(self, obj):
        return '<br>'.join([issues.issue_type for issues in obj.issues.all()])

    issues_display.short_description = 'Issues'


class Stations(admin.ModelAdmin):
    list_display = ('type', 'line', 'number')
    list_filter = ('type',)


class Scores(admin.ModelAdmin):
    list_display = ('user', 'station_type', 'previous', 'current', 'estimated')
    list_filter = ('station_type',)


admin.site.register(StationType, StationTypes)
admin.site.register(Station, Stations)
admin.site.register(IssueLog, IssueLogs)
admin.site.register(OccupationLog, OccupationLogs)
admin.site.register(Score, Scores)