# Generated by Django 4.2.2 on 2025-01-13 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0004_alter_media_caption_alter_media_name_alter_note_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='time_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='note',
            name='time_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='point',
            name='time_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
