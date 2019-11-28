from django.db import models
from django.contrib.auth.models import User

# new profile signal
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('not_specified', 'Not Specified'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to='upload/', blank=True, null=True)
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES, default='not_specified')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
