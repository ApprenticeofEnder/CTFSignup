from django.core.exceptions import ValidationError
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    team_cap = models.IntegerField()

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Create your models here.
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    discord_handle = models.CharField(max_length=100)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    premade_team_name = models.CharField('Premade Team Name (OPTIONAL)', max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if self.__class__.objects.\
                filter(email=self.email, event=self.event).\
                exists():
            raise ValidationError(
                message=f'User {self.email} has already signed up for event {self.event}',
                code='unique_together',
            )
    
    def clean(self, *args, **kwargs):
        if not self.email.endswith("carleton.ca"):
            raise ValidationError(
                message=f'{self.email} is not a valid Carleton email address',
                code='unique_together',
            )