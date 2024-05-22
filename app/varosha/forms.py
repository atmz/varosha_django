from django import forms
from django.forms import ModelForm

from .models import Person, Point, Media


class PersonForm(ModelForm):
     class Meta:
         model = Person
         exclude = []

class PersonDeleteForm(ModelForm):
     class Meta:
         model = Person
         fields = ["id"]
         widgets = {'id': forms.HiddenInput()}

class PointForm(ModelForm):
     class Meta:
         model = Point
         fields = ["x", "y", "name", "name_gr", "type"]

class PointAddFromMapForm(ModelForm):
    persons = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
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