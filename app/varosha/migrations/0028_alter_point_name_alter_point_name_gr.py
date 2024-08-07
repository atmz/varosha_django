# Generated by Django 4.2.2 on 2024-07-16 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0027_alter_person_birth_year_alter_person_death_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Name in English'),
        ),
        migrations.AlterField(
            model_name='point',
            name='name_gr',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Name in Greek'),
        ),
    ]
