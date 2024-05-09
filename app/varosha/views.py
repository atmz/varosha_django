from django.http import HttpResponseRedirect
from django.shortcuts import render

from .settings import MEDIA_URL

from .models import Media, Point
from .forms import MediaForm, PointForm


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
        media = list(p.media_set.all())[0] if p.media_set.count()>0 else None 
        context["point_data"].append({
            'x':p.x,
            'y':p.y,
            'name':p.name,
            'media': {
                'url': f"{MEDIA_URL}{media.path}"
            }
        })
    return render(request, "index.html", context)
