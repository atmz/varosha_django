from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


from .models import Point, Media, Note


class PointForm(ModelForm):
     class Meta:
        model = Point
        fields = ['x', 'y', 'name']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'note-field', 'rows': 3, 'placeholder': _('Add note, memory or name'),'cols':30}),
        }

class PointEditForm(ModelForm):
    class Meta:
        model = Point
        fields = ["id", "x", "y", "name"]
        widgets = {
            'id': forms.HiddenInput(), 
            'x': forms.HiddenInput(), 
            'y': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'name-field', 'placeholder': _('Name')}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class PointDeleteForm(ModelForm):
     class Meta:
         model = Point
         fields = ["id"]
         widgets = {'id': forms.HiddenInput()}

class MediaForm(ModelForm):
     class Meta:
         model = Media
         fields = ["file", "point"]


class UserChatBotAIConversationSendMessageForm(forms.Form):
    conversation_id = forms.IntegerField()
    user_message = forms.CharField(widget=forms.Textarea)