# Generated by Django 4.2.2 on 2024-06-07 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0021_alter_media_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='media',
            field=models.ManyToManyField(related_name='persons', to='varosha.media'),
        ),
    ]
