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
    path("", views.index, name="index"),
    path("point-form/", views.point_form, name="point-form"),
    path("point-form/<int:point_id>/", views.point_form, name="point-form"),
    path('delete-point/<int:point_id>/', views.delete_point, name='delete_point'),
    path("person-form/", views.person_form, name="person_form"),
    path('person-form/<int:person_id>/', views.person_form, name='person_form'),
    path("person-form-ajax/", views.person_form_ajax, name="person-form-ajax"),
    path('delete-person/<int:person_id>/', views.delete_person, name='delete_person'),
    path('delete-media/<int:media_id>/', views.delete_media, name='delete_media'),
    path("add-point-form/", views.point_add_from_map_form, name="add-point-form"),
    path("media-form/", views.media_form, name="media-form"),
    path('admin/', admin.site.urls),
    path('el/', views.set_language_to_greek, name='set_language_greek'),
    path('link-form-ajax/', views.link_form_ajax, name='link-form-ajax'),
    path('chat-bot-ai-send-message/', views.user_chat_bot_ai_conversation_send_message, name='user_chat_bot_ai_conversation_send_message'),
    path('get-conversation/<int:conversation_id>/', views.get_conversation, name='get_conversation'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
