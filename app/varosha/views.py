import json
import os
import re
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from django.utils.translation import gettext as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login, logout
from django.utils.translation import activate
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required


from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.http import require_POST

from .utils import get_client_ip

from .models import Media, Note, Point
from .forms import MediaForm, NoteForm, PointEditForm, PointForm

from .settings import MEDIA_URL
from django.conf import settings
import logging
from django.template import loader

logger = logging.getLogger('varosha') 

def _get_point_html(request, point):
    # Get existing notes
    point_form = PointEditForm(instance=point)
    note_form = NoteForm()
    existing_notes = Note.objects.filter(point=point)

    existing_media = Media.objects.filter(point=point)

    return loader.render_to_string('edit_point_form.html', {
        'point':point,
        'point_form': point_form,
        'note_form': note_form,
        'existing_notes': existing_notes,
        'existing_media': existing_media,
    }, request)

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
    point.ip_address = get_client_ip(request)
    if request.user.is_authenticated:
        point.creator = request.user
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
        return HttpResponse(_get_point_html(request, point))

    

def media_form(request):
    if request.method == "POST":
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            original_file = request.FILES['file']
            file_ext = os.path.splitext(original_file.name)[1].lower()
            if form.cleaned_data['point']:
                point_id = form.cleaned_data['point'].id
            else:
                point_id = "no_point"
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
            media.ip_address = get_client_ip(request)
            if request.user.is_authenticated:
                media.creator = request.user
            media.save()
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
            'html':_get_point_html(request, p)
        }
        context["point_data"].append(point_data)
    return render(request, "index.html", context)

def set_language_to_greek(request):
    activate('el')  # Activate the Greek language
    response = HttpResponseRedirect(reverse('index'))  # Redirect to the index page
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'el')
    return response


def media_gallery(request):
    media_list = Media.objects.select_related('point').all().order_by("point__y")
    return render(request, 'media_gallery.html', {'media_list': media_list})



def feed(request):
    feed = list(Media.objects.select_related('point').all().order_by("-time_added"))
    feed+=list( Note.objects.select_related('point').all().order_by("-time_added"))
    feed.sort(key=lambda x: x.time_added, reverse=True)
    return render(request, 'media_gallery.html', {'media_list': feed})



def set_image_location(request, image_id):
    # Get the image by ID
    image = get_object_or_404(Media, id=image_id)
    
    context = {
        'image_id': image_id,
        'image_url': image.file.url,  # URL to the uploaded image
    }
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
            'html':_get_point_html(request, p)
        }
        context["point_data"].append(point_data)
    return render(request, "set_location.html", context)


def associate_image_with_point(request, image_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            point_id = data.get('point_id')
            lat = data.get('lat')
            lng = data.get('lng')

            # Get the image
            image = get_object_or_404(Media, id=image_id)

            if point_id:
                # Associate with an existing point
                point = get_object_or_404(Point, id=point_id)
            else:
                # Create a new point
                point = Point.objects.create(x=lng, y=lat)

            # Associate the image with the point
            image.point = point
            image.save()

            return JsonResponse({'status': 'success', 'message': 'Image associated successfully!', 'point_id': point.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def update_media_field(request, media_id):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')

        try:
            media = Media.objects.get(id=media_id)

            if field in ['name', 'caption']:
                setattr(media, field, value)
                media.save()
                return JsonResponse({'status': 'success', 'message': f'{field} updated successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid field.'})
        except Media.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Media not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)

    # Ensure only creator or superuser can delete
    if request.user == point.creator or request.user.is_superuser:
        point.delete()
        return redirect('index')  # Redirect to map or home

    return HttpResponseForbidden("You are not allowed to delete this point.")



@login_required
def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    # Ensure only creator or superuser can delete
    if request.user == media.creator or request.user.is_superuser:
        media.delete()
        return redirect('media_gallery')  # Redirect after deletion

    return HttpResponseForbidden("You are not allowed to delete this media.")



def create_superuser(request):
    username = 'admin'
    email = 'alex.toumazis+admin@gmail.com'
    from django.contrib.auth.models import User
    from varosha.settings import SUPER_USER_PASS
    if User.objects.filter(username=username).exists() or not SUPER_USER_PASS:
        pass
    else:
        User.objects.create_superuser(username=username, email=email, password=SUPER_USER_PASS)