from django.db import models
from groups.models import Group
from django.contrib.auth.models import User

class Event(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')
    subject = models.CharField(max_length=20)
    description = models.TextField(max_length=200, null=True, blank=True)

    is_fixed = models.BooleanField(default=False)

    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.group.name + " - " + self.subject
    
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participating')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')

    class Meta:
        unique_together = ['user', 'event']

    def __str__(self):
        return f"{self.event.group.name}/{self.event.subject} - {self.user.username}"
    
class Vote(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='vote')
    deadline = models.DateTimeField()
    duration = models.PositiveIntegerField(default=2, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return self.event.group.name + " - " + self.event.subject
    
class VoteResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsed_votes')
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='responses')
    response_matrix = models.JSONField()

    class Meta:
        unique_together = ['user', 'vote']

    def __str__(self):
        return f"{self.vote.event.group.name}/{self.vote.event.subject} - {self.user.username}"
    
class VoteResult(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='results')
    
    start_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.vote.event.group.name}/{self.vote.event.subject}"