
from django.db import models
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger('varosha') 


class Point(models.Model):
    x = models.FloatField(verbose_name=_("Longitude"))  
    y = models.FloatField(verbose_name=_("Latitude"))
    name = models.CharField(max_length=100, verbose_name=_("Name"), null=True, blank=True)
    def __str__(self):
        return f"[{self.x},{self.y}]"
    
class Media(models.Model):
    file = models.FileField(upload_to='uploads/')  # Path in S3 where files will be stored
    point = models.ForeignKey("Point", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name=_("Name"), null=True, blank=True)
    caption = models.CharField(max_length=100, verbose_name=_("Caption"), null=True, blank=True)
    @property
    def path(self):
        return self.file.url

class Note(models.Model):
    text = models.TextField(verbose_name=_("Note"), blank=True)
    point = models.ForeignKey("Point", on_delete=models.CASCADE, null=False)



# class Conversation(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     language = models.CharField(max_length=2, choices=[
#         ('en', 'English'),
#         ('el', 'Greek')
#     ])
#     is_over = models.BooleanField(default=False)

# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
#     sender = models.CharField(max_length=16, choices=[
#         ('model', 'Model'),
#         ('user', 'User')
#     ])
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
