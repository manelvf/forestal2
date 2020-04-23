from django.contrib.auth.models import User
from django.utils.encoding import smart_text
import datetime

from django.db import models
from django import forms


class Memento(models.Model):
    app = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    data = models.TextField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.app + " : " + self.model + " - " + unicode(self.date) + " - " + unicode(self.user)



