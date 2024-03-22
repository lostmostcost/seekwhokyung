from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField
from common.utils import UniqueFilenameGenerator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=5)
    phone_number = PhoneNumberField(region='KR', blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to=UniqueFilenameGenerator('profile_images'), blank=True, null=True, default='profile_images/default.jpg')

    def __str__(self) :
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class ScheduleManager(models.Manager):
    def create_schedule(self, user, subject, schedule_matrix=None):

        if self.filter(user=user).count() >= 3:
            raise ValueError("사용자당 최대 3개의 스케줄을 가질 수 있습니다.")

        # 가장 큰 number 값 찾기
        max_number = self.filter(user=user).aggregate(models.Max('number'))['number__max']
        if max_number is None:
            max_number = 0
 
        # schedule_matrix가 제공되지 않은 경우, 기본값으로 1로 초기화된 행렬 생성
        if schedule_matrix is None:
            schedule_matrix = [[1] * 48 for _ in range(7)]

        # 새 스케줄 생성
        schedule = self.create(user=user, subject=subject, number=max_number + 1, schedule_matrix=schedule_matrix)

        return schedule

    def delete_schedule(self, schedule):
        # 삭제된 스케줄보다 큰 number 값을 가진 스케줄들의 number 값을 1씩 감소
        deleted_number = schedule.number
        schedule.delete()
        self.filter(user=schedule.user, number__gt=deleted_number).update(number=models.F('number') - 1)

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule')
    number = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=10, blank=True, null=True)
    schedule_matrix = models.JSONField()

    objects = ScheduleManager()

    class Meta:
        unique_together = ['user', 'number']

    def __str__(self):
        return f"{self.user.username} - Schedule[{self.number}]"