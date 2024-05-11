from django import forms
from django.forms import ModelForm

from .models import Point, Media


class PointForm(ModelForm):
     class Meta:
         model = Point
         fields = ["x", "y", "name", "name_gr", "type"]

class PointAddFromMapForm(ModelForm):
     class Meta:
         model = Point
         fields = ["x", "y", "name","name_gr", "type"]
         widgets = {'x': forms.HiddenInput(), 'y': forms.HiddenInput()}

class PointDeleteForm(ModelForm):
     class Meta:
         model = Point
         fields = ["id"]
         widgets = {'id': forms.HiddenInput()}

class MediaForm(ModelForm):
     class Meta:
         model = Media
         fields = ["file", "source", "point"]