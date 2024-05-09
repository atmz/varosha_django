from django.db import models

class Media(models.Model):
    path = models.CharField(max_length=64)
    source = models.CharField(max_length=64)
    point = models.ForeignKey("Point", on_delete=models.CASCADE)

class Person(models.Model):
    name = models.CharField(max_length=64)
    birth_year = models.CharField(max_length=4)
    death_year = models.CharField(max_length=4)
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    point = models.ForeignKey("Point", on_delete=models.CASCADE,)

class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    name = models.CharField(max_length=30)
    STATUS_CHOICES = [
        ("P", "Pending",),
        ("A", "Approved",)
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="P")
    def __str__(self):
        return f"{self.name} - [{self.x},{self.y}]"

    