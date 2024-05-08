from django.db import models

class Media(models.Model):
    path = models.CharField(max_length=64)
    source = models.CharField(max_length=64)
    media = models.ForeignKey("Point", on_delete=models.CASCADE)

class Person(models.Model):
    name = models.CharField(max_length=64)
    birth_year = models.CharField(max_length=4)
    death_year = models.CharField(max_length=4)
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    media = models.ForeignKey("Point", on_delete=models.CASCADE)

class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    name = models.CharField(max_length=30)


    