# Generated by Django 4.2.2 on 2024-05-10 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0004_remove_media_type_point_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name_gr',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='point',
            name='name_gr',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
