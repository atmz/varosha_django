# Generated by Django 4.2.2 on 2024-06-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0016_conversation_media_date_media_description_el_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='is_over',
            field=models.BooleanField(default=False),
        ),
    ]
