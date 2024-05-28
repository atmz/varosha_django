import os
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Media, Person, Point
from .forms import MediaForm, PointAddFromMapForm, PointDeleteForm, PointForm, PersonForm, PersonDeleteForm, PointLinkForm

from .settings import MEDIA_URL
from django.conf import settings

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

def person_form(request, person_id=None):
    if person_id:
        person = get_object_or_404(Person, id=person_id)
    else:
        person = None

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect("/person-form")   # Redirect to the form page after saving
    else:
        form = PersonForm(instance=person)

    return render(request, "person_form.html", {"form": form, "persons": Person.objects.all()})


def person_form_ajax(request):
    form = PersonForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": "saved person"})
    return JsonResponse({"error": "failed to save"})


def link_form_ajax(request):
    if request.method == 'POST':
        form = PointLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            point_id = request.POST.get('point_id')
            point = get_object_or_404(Point, id=point_id)
            link.point = point
            link.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return redirect("/person-form")  # Redirect to your form page after deletion

def delete_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    media.delete()
    return redirect("/media-form")  # Redirect to your form page after deletion


def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    point.delete()
    return redirect("/point-form")  # Redirect to your form page after deletion


def point_add_from_map_form(request, point_id=None):
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
            point = form.save()
            point.persons.set(form.cleaned_data['persons'])
            return HttpResponseRedirect(reverse('index')) 
    # if a GET (or any other method) we'll create a blank form
    else:
        x = request.GET["x"]
        y = request.GET["y"]
        if "id" in request.GET:
            point = get_object_or_404(Point,id=request.GET["id"])
            form = PointAddFromMapForm(instance=point,
            initial = {
                'persons': point.persons.all(),  # Set the initial value for persons field
            }
        )
        else:
            form = PointAddFromMapForm(initial={
                "x":x,
                "y":y
            })


    return render(request, "add_point_from_map_form.html", {"form": form, "points": Point.objects.all()})

def media_form(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        import logging
        logging.basicConfig(level=logging.DEBUG)
        # create a form instance and populate it with data from the request:
        form = MediaForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MediaForm()

    return render(request, "media_form.html", {"form": form, "media": Media.objects.all()})

def index(request):
    context = {}
    context["point_data"] = []
    for p in Point.objects.all():
        point_data = {
            'id':p.id,
            'x':p.x,
            'y':p.y,
            'name':p.name,
            'name_gr':p.name_gr,
        }
        media = p.media_set.all()
        if media.exists():
            point_data['media'] = [{'url': m.path} for m in media]
        else:
            point_data['media'] = []
             # Include associated links
        links = p.links.all()
        point_data['links'] = [{'name': link.name, 'url': link.url} for link in links]
        # Include associated people with birth and death dates
        associated_people = p.persons.all()
        point_data['people'] = [
            {
                'name': person.name,
                'name_gr': person.name_gr,
                'birth_year': person.birth_year,
                'death_year': person.death_year
            } for person in associated_people
        ]
        point_data['people'] = [] # No people for now
        context["point_data"].append(point_data)
    return render(request, "index.html", context)

def set_language_to_greek(request):
    activate('el')  # Activate the Greek language
    response = HttpResponseRedirect(reverse('index'))  # Redirect to the index page
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'el')
    return response