import datetime
import django
from django import forms
from django.db import models
from django.forms import ModelForm


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField("Name", max_length=200)
    deadline = models.DateTimeField("Due", 'completion date')
    category = models.ForeignKey(Category, null=True, blank=True)

class TodoItem(models.Model):
    parent = models.ForeignKey(Goal)
    name = models.CharField("Task", max_length=200)
    is_current = models.BooleanField("Current")
    is_complete = models.BooleanField("Done")
    
