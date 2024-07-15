from django.contrib import admin
from .models import *

admin.site.register(Media)
admin.site.register(Point)
admin.site.register(Person)
admin.site.register(PointLink)
admin.site.register(Conversation)
admin.site.register(Message)