# Generated by Django 4.2.2 on 2024-05-22 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0011_remove_person_parents_remove_person_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_from_father', to='varosha.person'),
        ),
        migrations.AddField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_from_mother', to='varosha.person'),
        ),
    ]
