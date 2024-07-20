from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Person, Point, Media, PointLink


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
        fields = ['x', 'y', 'name', 'name_gr', 'status', 'type']

class PointAddFromMapForm(ModelForm):
    # persons = forms.ModelMultipleChoiceField(
    #     queryset=Person.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )
    class Meta:
        model = Point
        fields = ["id", "x", "y", "name","name_gr", "type"]
        widgets = {
            'id': forms.HiddenInput(), 
            'x': forms.HiddenInput(), 
            'y': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'name-field'}),
            'name_gr': forms.TextInput(attrs={'class': 'name-field'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'P'  # Set status to "Pending"
        if commit:
            instance.save()
        return instance

class PersonFormForPointAddFromMapForm(ModelForm):
     class Meta:
        model = Person
        exclude = ["points", "media","mother","father"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'name-field'}),
            'name_gr': forms.TextInput(attrs={'class': 'name-field'}),
            'birth_year': forms.TextInput(attrs={'class': 'date-field'}),
            'death_year': forms.TextInput(attrs={'class': 'date-field'}),
        }

PersonFormSet = forms.modelformset_factory(Person, form=PersonFormForPointAddFromMapForm, extra=0, can_delete=True)


class PointDeleteForm(ModelForm):
     class Meta:
         model = Point
         fields = ["id"]
         widgets = {'id': forms.HiddenInput()}

class MediaForm(ModelForm):
     class Meta:
         model = Media
         fields = ["file", "source", "point"]

class PointLinkForm(forms.ModelForm):
    class Meta:
        model = PointLink
        fields = ['name', 'url']


class UserChatBotAIConversationSendMessageForm(forms.Form):
    conversation_id = forms.IntegerField()
    user_message = forms.CharField(widget=forms.Textarea)