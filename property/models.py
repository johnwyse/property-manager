from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    tenant = models.BooleanField(default=True)
    manager = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senders")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipients")
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.URLField(blank=True, default='', max_length=1000)
    text = models.TextField(max_length=1000, default=" ", null=False, blank=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message #{self.id} to {self.recipient} from {self.sender}"
    
    def serialize(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "text": self.text,
            "timestamp": self.timestamp,
        }



class Unit(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managers")
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenants", blank=True, null=True)
    address = models.CharField(max_length=200)
    image = models.URLField(blank=True, default='', max_length=1000)
    # lease_document = file upload of pdfs

    def __str__(self):
        return f"{self.address}"    
    
    def serialize(self):
        return {
            "manager": self.manager,
            "tenant": self.tenant,
            "address": self.address,
            "image": self.image
        }



class Issue(models.Model):
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="issues")
    image = models.URLField(blank=True, default='', max_length=1000)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=False, blank=False)
    time_created = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.unit_id}"
    
    def serialize(self):
        return {
            "unit_id": self.unit_id,
            "image": self.image,
            "title": self.title,
            "description": self.description,
            "time_created": self.time_created,
            "resolved": self.resolved,
        }






    

