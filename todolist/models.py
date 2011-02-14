import datetime
import django
from django import forms
from django.db import models
from django.forms import ModelForm

class Goal(models.Model):
    name = models.CharField("Name", max_length=200)
    deadline = models.DateTimeField("Due", 'completion date')


class TodoItem(models.Model):
    parent = models.ForeignKey(Goal)
    name = models.CharField("Task", max_length=200)
    is_current = models.BooleanField("Current")
    is_complete = models.BooleanField("Done")

    