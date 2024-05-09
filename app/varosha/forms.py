from django.forms import ModelForm

from .models import Point, Media


class PointForm(ModelForm):
     class Meta:
         model = Point
         fields = ["x", "y", "name"]

class MediaForm(ModelForm):
     class Meta:
         model = Media
         fields = ["path", "source", "point"]