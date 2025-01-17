import json
import os
import re
from django.db.models import Q
from django.utils import timezone

from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.utils.translation import activate
from django.utils.translation import get_language

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.http import require_POST

from .models import Media, Note, Point
from .forms import MediaForm, NoteForm, PointEditForm, PointForm

from .settings import MEDIA_URL
from django.conf import settings
import logging

logger = logging.getLogger('varosha') 

def point_form(request, point_id=None):
    # if this is a POST request we need to process the form data
    if point_id:
        point = get_object_or_404(Point, id=point_id)
    else:
        point = None

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PointForm(request.POST, instance=point)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PointForm(instance=point)

    return render(request, "point_form.html", {"form": form, "points": Point.objects.all()})


def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    media.delete()
    return redirect("/media-form")  # Redirect to your form page after deletion


def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    point.delete()
    return redirect("/point-form")  # Redirect to your form page after deletion

def create_point(request):
    x = request.GET.get('x')
    y = request.GET.get('y')
    point = Point(x=x, y=y)
    point.save()
    return redirect(f'edit-point/{point.id}/')    


def edit_point(request, point_id=None):
    associated_people = False
    point = get_object_or_404(Point, id=point_id)
    if request.method == 'POST':
        point_form = PointEditForm(request.POST, instance=point)
        note_form = NoteForm(request.POST)

        if point_form.is_valid():
            point = point_form.save()
            if note_form.is_valid() and note_form.cleaned_data.get('text'):  # Only save if there's text
                note = note_form.save(commit=False)
                note.point = point
                note.save()


        else:
            logger.debug(f"PointAddFromMapForm: {point_form.errors}")

        return redirect(f'{reverse("index")}?lat={point.x}&lng={point.y}')    
    else:
        point_form = PointEditForm(instance=point)
        note_form = NoteForm(request.POST)
    # Get existing notes
    existing_notes = Note.objects.filter(point=point)

    existing_media = Media.objects.filter(point=point)

    return render(request, 'edit_point_form.html', {
        'point_form': point_form,
        'note_form': note_form,
        'existing_notes': existing_notes,
        'existing_media': existing_media,

    })

    

def media_form(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            original_file = request.FILES['file']
            file_ext = os.path.splitext(original_file.name)[1].lower()
            point_id = form.cleaned_data['point'].id
            timestamp =  timezone.now().strftime('%Y%m%d_%H%M%S')

            # Check if this is a pasted image or regular upload
            if original_file.name == 'blob': # Pasted images typically come as 'blob'
                new_filename = f'point_{point_id}_{timestamp}{file_ext}'
            else:
                # Keep original filename but add point_id and timestamp
                original_name = os.path.splitext(original_file.name)[0]
                new_filename = f'point_{point_id}_{timestamp}_{original_name}{file_ext}'
           
            form.instance.file.name = new_filename
            media = form.save()

            # Get the current language
            current_language = get_language()

            # # Start a new conversation for the uploaded media with the current language
            # conversation = Conversation.objects.create(point=media.point, media=media, language=current_language)
            # conversation.initialize()
            
            return JsonResponse({'success': True, 
                'media_url': media.file.url,  # Assuming you have a media model with a file field
                'message': 'Upload successful'})
        else:
            return JsonResponse({'success': False, 'error': form.errors})

    else:
        form = MediaForm()

    return render(request, "media_form.html", {"form": form, "media": Media.objects.all()})

# def create_new_point_conversation(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         type = data.get('type')
#         x = data.get('x')
#         y = data.get('y')

#         # Get the current language
#         current_language = get_language()

#         point =  Point.objects.create(
#             x=x,
#             y=y,
#             type=type,
#             status='U'
#         )
#         # Start a new conversation for the uploaded media with the current language
#         conversation = Conversation.objects.create(point=point, language=current_language)
#         conversation.initialize()
        
#         return JsonResponse({'success': True, 'conversation_id': conversation.id})

#     return JsonResponse({'success': False})

def index(request):
    username = 'admin'
    email = 'alex.toumazis+admin@gmail.com'
    from django.contrib.auth.models import User
    from varosha.settings import SUPER_USER_PASS
    if User.objects.filter(username=username).exists() or not SUPER_USER_PASS:
        pass
    else:
        User.objects.create_superuser(username=username, email=email, password=SUPER_USER_PASS)

    context = {}
    context["point_data"] = []
    for p in  Point.objects.filter(
        Q(name__isnull=False) & ~Q(name='') |
        Q(media__isnull=False) |
        Q(note__isnull=False)
    ):
        point_data = {
            'id':p.id,
            'x':p.x,
            'y':p.y,
            'name':p.name,
        }
        context["point_data"].append(point_data)
    return render(request, "index.html", context)

def set_language_to_greek(request):
    activate('el')  # Activate the Greek language
    response = HttpResponseRedirect(reverse('index'))  # Redirect to the index page
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'el')
    return response

@require_POST
def user_chat_bot_ai_conversation_send_message(request):
    form = UserChatBotAIConversationSendMessageForm(request.POST)
    if form.is_valid():
        conversation_id = form.cleaned_data['conversation_id']
        user_message = form.cleaned_data['user_message']
        
        conversation = get_object_or_404(Conversation, id=conversation_id)
        conversation.send_message(user_message)
        
        # Retrieve the conversation messages
        messages = conversation.messages.all().values('sender', 'text', 'timestamp')
        
        return JsonResponse({'messages': list(messages), 'is_over': conversation.is_over}, status=200)
    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    

def get_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    messages = conversation.messages.all().values('id','sender', 'text', 'timestamp')
    localized_messages = []
    for message in messages:
        if message['sender'] == 'user':
            sender = _('You')
        elif message['sender'] == 'model':
            sender = _('AI Helper')
        else:
            sender = message['sender']  # Fallback in case there are other senders
        localized_messages.append({
            'id': message['id'],
            'sender': sender,
            'text': message['text']
        })
    type =  "media" if conversation.media else "point"
    if type == "media":
        return JsonResponse({
            'conversation_id': conversation.id,
            'messages': localized_messages,
            'type': 'media',
            'media_path': conversation.media.path,
            'is_over': conversation.is_over,
            })
    elif type == "point":
        return JsonResponse({
            'conversation_id': conversation.id,
            'messages': localized_messages,
            'type': 'point',
            'point_id': conversation.point.id,
            'is_over': conversation.is_over,
        })


def conversations_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'conversations_list.html', {'conversations': conversations})

@require_POST
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.delete()
    return redirect(reverse('conversations_list'))


def media_gallery(request):
    media_list = Media.objects.select_related('point').all().order_by("point__y")
    return render(request, 'media_gallery.html', {'media_list': media_list})



def feed(request):
    feed = list(Media.objects.select_related('point').all().order_by("time_added"))
    feed+=list( Note.objects.select_related('point').all().order_by("time_added"))
    feed.sort(key=lambda x: x.time_added)
    return render(request, 'media_gallery.html', {'media_list': feed})