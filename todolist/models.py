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
    
    
class Tag(models.Model):
    goal = models.ForeignKey(Goal)
    name = models.CharField(max_length=100)
    
    def color(self):
        name_hash = hash(self.name)
        
        red = name_hash & 0xFF
        green = (name_hash << 0xFF) & 0xFF
        blue = (name_hash << 0xFFFF) & 0xFF
        
        make_light_color = lambda x: x / 3 + 0xAA
        
        red = make_light_color(red)
        green = make_light_color(green)
        blue = make_light_color(blue)
        
        return 'rgb(%s,%s,%s)' % (red, green, blue)
        

    