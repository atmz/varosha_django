from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Media, Person, Point
from .forms import MediaForm, PointAddFromMapForm, PointDeleteForm, PointForm, PersonForm, PersonDeleteForm

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

def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return redirect("/person-form")  # Redirect to your form page after deletion


def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    point.delete()
    return redirect("/point-form")  # Redirect to your form page after deletion


def point_add_from_map_form(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PointAddFromMapForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            point = form.save()
            print(form.cleaned_data['persons'])
            point.persons.set(form.cleaned_data['persons'])
            return HttpResponseRedirect(reverse('index'))  # Redirect to the index page

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
        # create a form instance and populate it with data from the request:
        import boto3
        from botocore.exceptions import NoCredentialsError, PartialCredentialsError

        s3 = boto3.client('s3')

        try:
            response = s3.list_buckets()
            print("S3 Buckets:", response['Buckets'])
        except NoCredentialsError:
            print("Credentials not available")
        except PartialCredentialsError:
            print("Incomplete credentials provided")
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
        media = list(p.media_set.all())[0] if p.media_set.count()>0 else None
        if media:
            point_data['media'] =  {
                'url': f"{MEDIA_URL}{media.path}"
            }
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
        context["point_data"].append(point_data)
    return render(request, "index.html", context)

def set_language_to_greek(request):
    activate('el')  # Activate the Greek language
    response = HttpResponseRedirect(reverse('index'))  # Redirect to the index page
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'el')
    return response