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
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('el/', views.set_language_to_greek, name='set_language_greek'),
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("create-point", views.create_point, name="create-point"),
    path("edit-point/<int:point_id>/", views.edit_point, name="edit-point-form"),
    path("point-form/", views.point_form, name="point-form"),
    path("point-form/<int:point_id>/", views.point_form, name="point-form"),
    path('delete-point/<int:point_id>/', views.delete_point, name='delete_point'),
    path("media-form/", views.media_form, name="media-form"),
    path('delete-media/<int:media_id>/', views.delete_media, name='delete_media'),
    path('media-gallery/', views.media_gallery, name='media_gallery'),
    path('feed/', views.feed, name='feed'),
    path('associate-image/<int:image_id>/', views.associate_image_with_point, name='associate_image_with_point'),
    path('set-location/<int:image_id>/', views.set_image_location, name='set_location'),





]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
