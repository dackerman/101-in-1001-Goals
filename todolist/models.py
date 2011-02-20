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

    def percent_complete(self):
        tasks = TodoItem.objects.filter(parent=self)
        total_tasks = 0
        total_complete = 0
        for task in tasks:
            total_tasks += 1
            if task.is_complete:
                total_complete += 1
        if not total_tasks:
            return float(0)
        return 100 * total_complete / total_tasks

class TodoItem(models.Model):
    parent = models.ForeignKey(Goal)
    name = models.CharField("Task", max_length=200)
    is_current = models.BooleanField("Current")
    is_complete = models.BooleanField("Done")
    
