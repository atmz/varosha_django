# Generated by Django 4.2.2 on 2024-05-11 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0009_alter_point_name_alter_point_name_gr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='path',
        ),
        migrations.AddField(
            model_name='media',
            name='file',
            field=models.FileField(default='', upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
