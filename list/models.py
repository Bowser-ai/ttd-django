from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    text = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('list_view', args=[self.id])


class Item(models.Model):
    list = models.ForeignKey(List, default=None)
    text = models.TextField(default='')

    class Meta:
        unique_together = ('list', 'text')
        ordering = ('id',)

    def __str__(self):
        return self.text

