# Generated by Django 4.2.2 on 2024-05-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0013_alter_person_death_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='points',
            field=models.ManyToManyField(related_name='persons', to='varosha.point'),
        ),
    ]
