"""
URL configuration for varosha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from varosha import views

from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("", views.index, name="index"),
    path("point-form/", views.point_form, name="point-form"),
    path("add-point-form/", views.point_add_from_map_form, name="add-point-form"),
    path("media-form/", views.media_form, name="media-form"),
    path('delete-point/<int:point_id>/', views.delete_point, name='delete_point'),
    path('admin/', admin.site.urls),
    path('el/', views.set_language_to_greek, name='set_language_greek'),

]
