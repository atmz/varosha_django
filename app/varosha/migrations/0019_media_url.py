# Generated by Django 4.2.2 on 2024-06-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0018_alter_media_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='url',
            field=models.URLField(null=True, verbose_name='URL'),
        ),
    ]
