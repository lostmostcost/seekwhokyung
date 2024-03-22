from django.contrib import admin
from .models import Event, Participant, Vote, VoteResponse, VoteResult

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Vote)
admin.site.register(VoteResponse)
admin.site.register(VoteResult)