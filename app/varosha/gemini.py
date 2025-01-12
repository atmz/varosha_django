# import json
# import os
# import re
# import tempfile
# import requests
# import logging
# logger = logging.getLogger('varosha') 

# import mimetypes
# import google.generativeai as genai
# def _generate_display_name(self):
#     base_name = self.media.file.name.split('//')[-1]
#     logger.debug(f"self.media.file.name - {self.media.file.name}")
#     unique_name = f"{self.media.id}_{base_name}"
#     logger.debug(f"_generate_display_name - {unique_name}")
#     return unique_name

# def _upload_media_file_to_gemini(self):
#     file_url = self.media.path
#     display_name = self._generate_display_name()
#     mime_type, _ = mimetypes.guess_type(display_name)

#     # Download the file from S3 to a local temporary file
#     response = requests.get(file_url)
#     logger.debug(f"Dowloaded file {file_url} from s3")
#     response.raise_for_status()  # Ensure we notice bad responses

#     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#         tmp_file.write(response.content)
#         tmp_file_path = tmp_file.name

#     try:
#         # Upload the local file to Google
#         logger.debug(f"genai.upload_file(path={tmp_file_path}, display_name={display_name}), mime_type={mime_type}")
#         file_response = genai.upload_file(path=tmp_file_path, display_name=display_name, mime_type=mime_type)
        
#         logger.debug(f"Uploaded file {file_response.display_name} as: {file_response.uri}")
#         logger.debug(f"Uploaded file {file_response.__dict__}")
#     finally:
#         # Ensure the temporary file is deleted
#         os.remove(tmp_file_path)

#     return file_response


# def _get_conversation_format_gemini_api_with_point(self):
#     if not GOOGLE_API_KEY: 
#         prompt_message = {
#             'role': 'user',
#             'parts': [get_add_point_prompt(self.point.type, self.language)]
#         }
#         messages = self.messages.all()
#         formatted_messages = [
#             prompt_message,
#             *[
#                 {'role': message.sender, 'parts': [message.text]}
#                 for message in messages
#             ]
#         ]
#         return formatted_messages

#     if self.language == 'el':
#         prompt_message = {
#             'role': 'user',
#             'parts': [get_add_point_prompt(self.point.type, self.language)]
#         }
#     else:  # Default to English if not Greek
#         prompt_message = {
#             'role': 'user',
#             'parts': [get_add_point_prompt(self.point.type, self.language)]
#         }
#     messages = self.messages.all()
#     formatted_messages = [
#         prompt_message,
#         *[
#             {'role': message.sender, 'parts': [message.text]}
#             for message in messages
#         ]
#     ]
#     return formatted_messages


# def _get_conversation_format_gemini_api_with_media(self):
#     if not GOOGLE_API_KEY: 
#         prompt_message = {
#             'role': 'user',
#             'parts': [prompt_en, get_point_prompt(self.media.point)]
#         }
#         messages = self.messages.all()
#         formatted_messages = [
#             prompt_message,
#             *[
#                 {'role': message.sender, 'parts': [message.text]}
#                 for message in messages
#             ]
#         ]
#         return formatted_messages

#     image = self._upload_media_file_to_gemini()
#     if self.language == 'el':
#         prompt_message = {
#             'role': 'user',
#             'parts': [prompt_el, get_point_prompt(self.media.point), image]
#         }
#     else:  # Default to English if not Greek
#         prompt_message = {
#             'role': 'user',
#             'parts': [prompt_en, get_point_prompt(self.media.point), image]
#         }
#     messages = self.messages.all()
#     formatted_messages = [
#         prompt_message,
#         *[
#             {'role': message.sender, 'parts': [message.text]}
#             for message in messages
#         ]
#     ]
#     return formatted_messages

# def _call_gemini_with_point(self):
#     # Get conversation format for the generative model
#     messages = self._get_conversation_format_gemini_api_with_point()


#     if not GOOGLE_API_KEY: 
#         response =  type("Foo",(object,),dict(text=f"fake response to {messages[-1]}"))
#     else:
#         # Initialize the generative model
#         model = genai.GenerativeModel('gemini-1.5-flash')

#         # Generate content using the model
#         logger.debug(f"Messages: {messages}")
#         response = model.generate_content(messages, 
#             safety_settings={
#                 HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
#             })

#     logger.debug(f"response: {response}")

#     # Extract JSON data from the response text
#     json_pattern = re.compile(r'<json>(.*?)</json>', re.DOTALL)
#     json_match = json_pattern.search(response.text)
    
#     if json_match:
#         json_data = json_match.group(1)
#         try:
#             response_data = json.loads(json_data)
#             if isinstance(response_data, dict):
#                 self.point.name = response_data.get('name', self.point.name)
#                 self.point.name_gr = response_data.get('name_gr', self.point.name_gr)
#                 for person_json in response_data.get('people', []):
#                     name = person_json.get('name', "")
#                     name_gr = person_json.get('name_gr', "")
#                     person = Person.objects.create(name=name, name_gr=name_gr)
#                     person.points.add(self.point)
#                     person.save()

#                 self.point.save()
#                 self.is_over = True
#                 self.save()
#                 Message.objects.create(
#                     conversation=self,
#                     sender='model',
#                     text=_("Thank you!")
#                 )            
#                 return 
#         except json.JSONDecodeError as e:
#                 logger.debug(f"JSONDecodeError: {e}")
#                 logger.debug(f"response.text: {response.text}")

#                 Message.objects.create(
#                     conversation=self,
#                     sender='model',
#                     text=_("Thank you!")
#                 )           
#                 return 

#     if not response.text.strip():
#         self.is_over = True
#         self.save()

#     # Append model response to the conversation
#     Message.objects.create(
#         conversation=self,
#         sender='model',
#         text=response.text
#     )           

#     return

# def _call_gemini_with_media(self):
#     # Get conversation format for the generative model
#     messages = self._get_conversation_format_gemini_api_with_media()


#     if not GOOGLE_API_KEY: 
#         response =  type("Foo",(object,),dict(text=f"fake response to {messages[-1]}"))
#     else:
#         # Initialize the generative model
#         model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

#         # Generate content using the model
#         logger.debug(f"Messages: {messages}")
#         response = model.generate_content(messages)


#     # Extract JSON data from the response text
#     json_pattern = re.compile(r'<json>(.*?)</json>', re.DOTALL)
#     json_match = json_pattern.search(response.text)
    
#     if json_match:
#         json_data = json_match.group(1)
#         try:
#             response_data = json.loads(json_data)
#             if isinstance(response_data, dict):
#                 self.media.date = response_data.get('date', self.media.date)
#                 self.media.description_en = response_data.get('description_en', self.media.description_en)
#                 self.media.description_el = response_data.get('description_el', self.media.description_el)
#                 self.media.type = response_data.get('type', self.media.type)
#                 self.media.source = response_data.get('source', self.media.source)
#                 self.media.url = response_data.get('url', self.media.url)
#                 self.media.email = response_data.get('email', self.media.email)
#                 self.media.save()
#                 self.is_over = True
#                 self.save()
#                 # Append model response to the conversation
#                 Message.objects.create(
#                     conversation=self,
#                     sender='model',
#                     text=_("Thank you! We have saved the information you provided for this image")
#                 )           
#                 return 
#         except json.JSONDecodeError:
#                 Message.objects.create(
#                     conversation=self,
#                     sender='model',
#                     text=_("Thank you!")
#                 )           
#                 return 

#     if not response.text.strip():
#         self.is_over = True
#         self.save()

#     # Append model response to the conversation
#     Message.objects.create(
#         conversation=self,
#         sender='model',
#         text=response.text
#     )           

#     return

# def initialize(self):
#     if not self.messages.exists():
#         if self.media:
#             return self._call_gemini_with_media()
#         else:
#             return self._call_gemini_with_point()

# def send_message(self, user_message):
#     # Append user message to the conversation
#     Message.objects.create(
#         conversation=self,
#         sender='user',
#         text=user_message
#     )
#     if self.media:
#         return self._call_gemini_with_media()
#     else:
#         return self._call_gemini_with_point()