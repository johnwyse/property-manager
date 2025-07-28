from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import base64


def image_to_base64(image_file):
    """Convert uploaded image file to base64 string"""
    if image_file:
        image_data = image_file.read()
        return base64.b64encode(image_data).decode('utf-8')
    return None


def file_to_base64(file_obj):
    """Convert any uploaded file to base64 string"""
    if file_obj:
        file_data = file_obj.read()
        return base64.b64encode(file_data).decode('utf-8')
    return None


def file_to_base64(file_obj):
    """Convert uploaded file to base64 string with filename"""
    if file_obj:
        file_data = file_obj.read()
        base64_data = base64.b64encode(file_data).decode('utf-8')
        return {
            'data': base64_data,
            'filename': file_obj.name,
            'content_type': getattr(file_obj, 'content_type', 'application/octet-stream')
        }
    return None


class User(AbstractUser):
    tenant = models.BooleanField(default=True)
    manager = models.BooleanField(default=False)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_images/')
    profile_picture_base64 = models.TextField(blank=True, null=True)

    def is_valid_user(self):
        return (self.manager == True and self.tenant == False) or (self.manager == False and self.tenant == True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senders")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipients")
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, null=True, upload_to='message_images/')
    image_base64 = models.TextField(blank=True, null=True)
    text = models.TextField(max_length=1000, default=" ", null=False, blank=False)
    read = models.BooleanField(default=False)

    def is_valid_message(self):
        a = (self.sender.manager == True and self.recipient.tenant == True) or (self.sender.tenant == True and self.recipient.manager == True)
        b = self.text != ""
        return a == True and b == True

    def __str__(self):
        return f"Message #{self.id} to {self.recipient} from {self.sender}"
    
    def serialize(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "text": self.text,
            "timestamp": self.timestamp,
            "read": self.read,
            "image": self.image
        }



class Unit(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managers")
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenants", blank=True, null=True)
    address = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='unit_images/')
    image_base64 = models.TextField(blank=True, null=True)
    lease = models.FileField(blank=True, upload_to='leases/')
    lease_base64 = models.TextField(blank=True, null=True)
    lease_base64 = models.JSONField(blank=True, null=True)  # Store filename, content_type, and data

    def is_valid_unit(self):
        return self.manager and self.manager.manager == True and self.manager.tenant == False and self.address != ""
   
    def __str__(self):
        return f"{self.address}"    
    
    def serialize(self):
        return {
            "manager": self.manager,
            "tenant": self.tenant,
            "address": self.address,
            "image": self.image,
            "lease": self.lease
        }



class Issue(models.Model):
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="issues")
    image = models.ImageField(blank=True, upload_to='issue_images/')
    image_base64 = models.TextField(blank=True, null=True)
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






    

