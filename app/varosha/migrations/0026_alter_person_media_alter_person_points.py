# Generated by Django 4.2.2 on 2024-07-16 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0025_alter_person_birth_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='media',
            field=models.ManyToManyField(blank=True, null=True, related_name='persons', to='varosha.media'),
        ),
        migrations.AlterField(
            model_name='person',
            name='points',
            field=models.ManyToManyField(blank=True, null=True, related_name='persons', to='varosha.point'),
        ),
    ]
