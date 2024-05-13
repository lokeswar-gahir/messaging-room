from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class RoomLink(models.Model):
    ip_address = models.GenericIPAddressField()
    link = models.SlugField(unique=True)
    first_message = models.TextField()
    link_password = models.CharField(max_length=25)
    is_open = models.BooleanField(default=True)
    verified_ips = models.CharField(max_length=60, default='127.0.0.1')

    def get_absolute_url(self):
        return reverse("main:room", kwargs={"link": self.link})
    
    def save(self, *args, **kwargs):
        super(RoomLink, self).save(*args, **kwargs)

class Messages(models.Model):
    ip_address = models.GenericIPAddressField()
    room_link = models.ForeignKey(RoomLink, on_delete=models.CASCADE, default='10')
    message = models.CharField(max_length=250)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        super(Messages, self).save(*args, **kwargs)
    class Meta:
        ordering = ['-recorded_at']

@receiver(post_save, sender=RoomLink)
def firstMessageEntry(sender, instance, created, **kwargs):
    if created:
        ip = instance.ip_address
        Messages.objects.create(ip_address = ip, room_link=instance, message = instance.first_message)

