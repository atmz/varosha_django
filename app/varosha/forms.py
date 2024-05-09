from django import forms
from django.forms import ModelForm

from .models import Point, Media


class PointForm(ModelForm):
     class Meta:
         model = Point
         fields = ["x", "y", "name"]

class PointAddFromMapForm(ModelForm):
     class Meta:
         model = Point
         fields = ["x", "y", "name"]
         widgets = {'x': forms.HiddenInput(), 'y': forms.HiddenInput()}

class MediaForm(ModelForm):
     class Meta:
         model = Media
         fields = ["path", "source", "point"]