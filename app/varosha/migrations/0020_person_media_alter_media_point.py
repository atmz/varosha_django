# Generated by Django 4.2.2 on 2024-06-06 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('varosha', '0019_media_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='media',
            field=models.ManyToManyField(related_name='media', to='varosha.media'),
        ),
        migrations.AlterField(
            model_name='media',
            name='point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='varosha.point'),
        ),
    ]