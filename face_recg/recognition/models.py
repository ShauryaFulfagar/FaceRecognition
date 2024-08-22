from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    embedding = models.BinaryField()

    def __str__(self):
        return self.name
