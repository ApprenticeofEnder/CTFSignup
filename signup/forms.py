from django import forms
from django.forms import ModelForm
from .models import TeamMember

class TeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        exclude = ['team', 'verified']
    
    def __init__(self, *args, **kwargs):
        super(TeamMemberForm, self).__init__(*args, **kwargs)
        self.fields['premade_team_name'].required = False