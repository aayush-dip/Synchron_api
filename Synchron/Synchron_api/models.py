from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    role = (("QA", "QA"), ("Developer", "Developer"), ("SM", "SM"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    position = models.CharField(max_length=15, choices=role, blank=False, default="Developer")

    def __str__(self):
        return "{0}".format(self.user.username)


class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return "{0}".format(self.team_name)

class StandupCard(models.Model):
    team_choices = [(team.id, team.team_name) for team in Team.objects.all()]
    created_by = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    release_cycle = models.CharField(max_length=20, null=False, blank=False)
    sprint_id = models.IntegerField(blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    remarks = models.TextField()
    teamname = models.ForeignKey(Team, on_delete=models.CASCADE, choices=team_choices)

    def __str__(self):
        return "{0}".format("Sprint Id number is  "+ str(self.sprint_id))

class MemberAndRemarks(models.Model):
    standup = models.ForeignKey(StandupCard, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    individual_remarks = models.TextField()

    def __str__(self):
        return "{0}".format("Sprint Id :"+str(self.standup.sprint_id) +" Name:"+ str(self.member.username))

