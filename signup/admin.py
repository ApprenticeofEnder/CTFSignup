from django.contrib import admin

# Register your models here.
from .models import TeamMember, Team, Event

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team']
    

class TeamAdmin(admin.ModelAdmin):
    list_display = ['event', 'name']

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)