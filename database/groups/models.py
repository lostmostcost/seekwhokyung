from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import uuid
from common.utils import UniqueFilenameGenerator

class Group(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=UniqueFilenameGenerator('group_images'), blank=True, null=True)
    president = models.ForeignKey(User, on_delete=models.CASCADE, related_name='president_groups', blank=True)
    create_date = models.DateTimeField(default=timezone.now, blank=True)
    invite_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def generate_invite_code(self, lenghth=20):
        return str(uuid.uuid4().hex[:20])

    def __str__(self):
        return self.name
    
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    
    class Meta:
        unique_together = ['user', 'group']

    def __str__(self):
        return f"{self.group.name} - {self.user.username}"