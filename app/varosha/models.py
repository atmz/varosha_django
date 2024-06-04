import json
import os
import re
import tempfile
from django.db import models
import google.generativeai as genai
import requests
from varosha.settings import GOOGLE_API_KEY

from varosha.prompts import prompt_el, prompt_en, get_point_prompt
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger('varosha') 
class Media(models.Model):
    file = models.FileField(upload_to='uploads/')  # Path in S3 where files will be stored
    source = models.CharField(max_length=64, choices=[
        ('own/family', 'Own/Family'),
        ('social media', 'Social Media'),
        ('unknown', 'Unknown')
    ], default="unknown")
    point = models.ForeignKey("Point", on_delete=models.CASCADE)
    date = models.CharField(max_length=16, default="")
    description_en = models.TextField(default="")
    description_el = models.TextField(default="")
    type = models.CharField(max_length=32, choices=[
        ('photo', 'Photo'),
        ('advertisement', 'Advertisement'),
        ('poster', 'Poster'),
        ('other', 'Other')
    ], default="photo")
    
    @property
    def path(self):
        return self.file.url

class Conversation(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, choices=[
        ('en', 'English'),
        ('el', 'Greek')
    ])
    is_over = models.BooleanField(default=False)

    def _generate_display_name(self):
        base_name = self.media.file.name.split('/')[-1]
        logger.debug(f"self.media.file.name - {self.media.file.name}")
        unique_name = f"{self.media.id}_{base_name}"
        logger.debug(f"_generate_display_name - {unique_name}")
        return unique_name

    # def _upload_media_file_to_gemini(self):
    #     display_name = self._generate_display_name()
    #     if not GOOGLE_API_KEY: 
    #         print("debug - display_name:{display_name}")
    #         return {}
        
    #     # existing_file_response = genai.get_file(display_name)
    #     # if existing_file_response:
    #     #     return existing_file_response
    #     file_path = self.media.path
    #     file_response = genai.upload_file(path=file_path, display_name=display_name)
    #     return file_response

    def _upload_media_file_to_gemini(self):
        file_url = self.media.path
        display_name = self._generate_display_name()

        # Download the file from S3 to a local temporary file
        response = requests.get(file_url)
        logger.debug(f"Dowloaded file {file_url} from s3")
        response.raise_for_status()  # Ensure we notice bad responses

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        try:
            # Upload the local file to Google
            logger.debug(f"genai.upload_file(path={tmp_file_path}, display_name={display_name})")
            file_response = genai.upload_file(path=tmp_file_path, display_name=display_name)
            
            logger.debug(f"Uploaded file {file_response.display_name} as: {file_response.uri}")
            logger.debug(f"Uploaded file {file_response.__dict__}")
        finally:
            # Ensure the temporary file is deleted
            os.remove(tmp_file_path)

        return file_response


    def _get_conversation_format_gemini_api(self):
        image = self._upload_media_file_to_gemini()
        if self.language == 'el':
            prompt_message = {
                'role': 'user',
                'parts': [prompt_el, get_point_prompt(self.media.point), image]
            }
        else:  # Default to English if not Greek
            prompt_message = {
                'role': 'user',
                'parts': [prompt_en, get_point_prompt(self.media.point), image]
            }
        messages = self.messages.all()
        formatted_messages = [
            prompt_message,
            *[
                {'role': message.sender, 'parts': [message.text]}
                for message in messages
            ]
        ]
        return formatted_messages
    
    def _call_gemini(self):
        # Get conversation format for the generative model
        messages = self._get_conversation_format_gemini_api()


        if not GOOGLE_API_KEY: 
            response =  type("Foo",(object,),dict(text=f"fake response to {messages[-1]}"))
        else:
            # Initialize the generative model
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Generate content using the model
            logger.debug(f"Messages: {messages}")
            response = model.generate_content(messages)


        # Append model response to the conversation
        Message.objects.create(
            conversation=self,
            sender='model',
            text=response.text
        )
        # Extract JSON data from the response text
        json_pattern = re.compile(r'<json>(.*?)</json>', re.DOTALL)
        json_match = json_pattern.search(response.text)
        
        if json_match:
            json_data = json_match.group(1)
            try:
                response_data = json.loads(json_data)
                if isinstance(response_data, dict):
                    self.media.date = response_data.get('date', self.media.date)
                    self.media.description_en = response_data.get('description_en', self.media.description_en)
                    self.media.description_el = response_data.get('description_el', self.media.description_el)
                    self.media.type = response_data.get('type', self.media.type)
                    self.media.source = response_data.get('source', self.media.source)
                    self.media.save()
                    self.is_over = True
                    self.save()
                    return _("Thank you! We have saved the information you provided for this image")
            except json.JSONDecodeError:
                pass

        if not response.text.strip():
            self.is_over = True
            self.save()

        return response.text
    
    def initialize(self):
        if not self.messages.exists():
            self._call_gemini()

    def send_message(self, user_message):
        # Append user message to the conversation
        Message.objects.create(
            conversation=self,
            sender='user',
            text=user_message
        )
        return self._call_gemini()

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=16, choices=[
        ('model', 'Model'),
        ('user', 'User')
    ])
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Person(models.Model):
    name = models.CharField(max_length=64)
    name_gr = models.CharField(max_length=64)
    birth_year = models.CharField(max_length=4)
    death_year = models.CharField(max_length=4, null=True, blank=True)
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_from_mother')
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_from_father')
    points = models.ManyToManyField('Point', related_name='persons')


    def __str__(self):
        return self.name

    def get_parents(self):
        return {
            "mother": self.mother,
            "father": self.father,
        }

    def get_children(self):
        return list(self.children_from_mother.all()) + list(self.children_from_father.all())

class Point(models.Model):
    x = models.FloatField(verbose_name=_("Longitude"))  
    y = models.FloatField(verbose_name=_("Latitude"))
    name_gr = models.CharField(max_length=30, verbose_name=_("Name in Greek"), blank=True, default='')
    name = models.CharField(max_length=30, verbose_name=_("Name in English"), blank=True, default='')
    STATUS_CHOICES = [
        ("P", _("Pending")),
        ("A", _("Approved")),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="P",
        verbose_name=_("Status")
    )
    TYPE_CHOICES = [
        ("H", _("Home")),
        ("B", _("Business")),
        ("O", _("Other")),
    ]
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="H",
        verbose_name=_("Type")
    )

    def __str__(self):
        return f"{self.name} - [{self.x},{self.y}]"

    
class PointLink(models.Model):
    point = models.ForeignKey(Point, related_name='links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_("Link Name"))
    url = models.URLField(verbose_name=_("URL"))