# Generated by Django 4.2.2 on 2024-05-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0006_alter_point_name_alter_point_name_gr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='name',
            field=models.CharField(default='', max_length=30, verbose_name='Name in English'),
        ),
        migrations.AlterField(
            model_name='point',
            name='name_gr',
            field=models.CharField(default='', max_length=30, verbose_name='Name in Greek'),
        ),
    ]
