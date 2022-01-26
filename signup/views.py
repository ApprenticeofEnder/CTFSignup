from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count
from .forms import TeamMemberForm
from .models import TeamMember, Team

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            discord_handle = form.cleaned_data['discord_handle']
            event = form.cleaned_data["event"]
            premade_team_name = form.cleaned_data["premade_team_name"]
            member = TeamMember(
                name=name,
                email=email,
                discord_handle=discord_handle,
                event=event,
                premade_team_name=premade_team_name
            )
            if premade_team_name:
                assigned_team = Team.objects.create(
                    name=f"{event} Premade",
                    event=event
                )
            else:
                assigned_team_qset = Team.objects.filter(event=event).annotate(members=Count('teammember')).filter(members__lt=event.team_cap)
                assigned_team = assigned_team_qset.first()
                if not assigned_team:
                    num_teams = len(event.team_set.all())
                    assigned_team = Team.objects.create(
                        name=f"{event} Team {num_teams + 1}",
                        event=event
                    )
            member.team = assigned_team
            member.save()
            response = HttpResponseRedirect(f"{reverse('success')}?event={event}")
            request.session["name"] = name
            request.session["email"] = email
            request.session["discord_handle"] = discord_handle
            return response
    else:
        form = TeamMemberForm()
    return render(request, 'signup.html', {'form': form})

def autofill(request):
    
    name = request.session["name"] if request.session.get("name") else ""
    email = request.session["email"] if request.session.get("email") else ""
    discord_handle = request.session["discord_handle"] if request.session.get("discord_handle") else ""
    
    return JsonResponse({
        "name": name,
        "email": email,
        "discord_handle": discord_handle
    })

def success(request):
    return render(request, 'success.html', {'event': request.GET.get("event")})