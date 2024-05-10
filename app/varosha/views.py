from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Media, Point
from .forms import MediaForm, PointAddFromMapForm, PointDeleteForm, PointForm

from .settings import MEDIA_URL
from django.conf import settings

def point_form(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PointForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PointForm()

    return render(request, "point_form.html", {"form": form, "points": Point.objects.all()})

def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    point.delete()
    return redirect("/point-form")  # Redirect to your form page after deletion


def point_add_from_map_form(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PointForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")

    # if a GET (or any other method) we'll create a blank form
    else:
        x = request.GET["x"]
        y = request.GET["y"]
        form = PointAddFromMapForm(initial={
            "x":x,
            "y":y
        })

    return render(request, "add_point_from_map_form.html", {"form": form, "points": Point.objects.all()})

def media_form(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = MediaForm(request.POST)
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
            'x':p.x,
            'y':p.y,
            'name':p.name,
            'name_gr':p.name_gr,
        }
        media = list(p.media_set.all())[0] if p.media_set.count()>0 else None
        if media:
            point_data['media'] =  {
                'url': f"{MEDIA_URL}{media.path}"
            }
        context["point_data"].append(point_data)
    return render(request, "index.html", context)

def set_language_to_greek(request):
    activate('el')  # Activate the Greek language
    response = HttpResponseRedirect(reverse('index'))  # Redirect to the index page or a specified URL
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'el')
    return response