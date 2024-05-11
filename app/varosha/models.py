from django.db import models
from django.utils.translation import gettext_lazy as _


class Media(models.Model):
    file = models.FileField(upload_to='uploads/')  # Path in S3 where files will be stored
    source = models.CharField(max_length=64)
    point = models.ForeignKey("Point", on_delete=models.CASCADE)
    @property
    def path(self):
        return self.file.url

class Person(models.Model):
    name = models.CharField(max_length=64)
    name_gr = models.CharField(max_length=64)
    birth_year = models.CharField(max_length=4)
    death_year = models.CharField(max_length=4)
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    point = models.ForeignKey("Point", on_delete=models.CASCADE,)

class Point(models.Model):
    x = models.FloatField(verbose_name=_("Longitude"))
    y = models.FloatField(verbose_name=_("Latitude"))
    name_gr = models.CharField(max_length=30, verbose_name=_("Name in Greek"), blank=True, default='')
    name = models.CharField(max_length=30, verbose_name=_("Name in English"), blank=True, default='')
    STATUS_CHOICES = [
        ("P", _("Pending")),
        ("A", _("Approved")),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="P",
        verbose_name=_("Status")
    )
    TYPE_CHOICES = [
        ("H", _("Home")),
        ("B", _("Business")),
        ("O", _("Other")),
    ]
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="H",
        verbose_name=_("Type")
    )

    def __str__(self):
        return f"{self.name} - [{self.x},{self.y}]"

    