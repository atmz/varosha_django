# Generated by Django 4.2.2 on 2025-01-12 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0002_remove_media_caption_gr_remove_media_name_gr_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='source',
        ),
    ]
