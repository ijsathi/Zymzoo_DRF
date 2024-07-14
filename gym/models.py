from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class GymUser(AbstractUser):
    is_staff_member = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='gymuser_set', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='gymuser_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Models for Membership and Subscription Management:
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    duration_in_days = models.IntegerField()
    def __str__(self):
        return self.name
    

class Member(models.Model):
    user = models.OneToOneField(GymUser, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Models for Fitness Classes and Scheduling
INTENSITY = [
    ("Low ", "Low"),
    ("Medium ", "Medium"),
    ("High", "High"),
]
class FitnessClass(models.Model):
    title = models.CharField(max_length=100)
    schedule = models.DateTimeField()
    duration_minutes_in_days = models.IntegerField(default=60)
    instructor = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gym/images', default='gym/images/default_image.jpg')
    intensity = models.CharField(choices=INTENSITY, max_length=20, default="Medium")
    def __str__(self):
        return self.title

class Booking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} booking {self.fitness_class}"