from django.db import models

class List(models.Model):
    text = models.TextField(default='')

class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    text = models.TextField(default='')

