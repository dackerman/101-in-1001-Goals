from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from todolist.models import Goal
from todolist.models import TodoItem
import datetime
from django import forms
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.core.context_processors import csrf

class GoalForm(ModelForm):
    deadline = forms.DateField(label="Due", initial=datetime.date.today)
    class Meta:
        model = Goal

def list_goals(request):
    if request.method == 'POST':
        goal = GoalForm(request.POST)
        goal.save()

    goals = Goal.objects.all()

    template_data = {
        'goals': goals,
        'goalform': GoalForm(),
    }
    template_data.update(csrf(request))
    return render_to_response('todolist/list_goals.html', template_data)
    

class TaskForm(ModelForm):
    class Meta:
        model = TodoItem
        exclude = ('parent',)
        widgets = {'name': forms.TextInput(attrs={'size':'70'})}


def view_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    TaskFormSet = modelformset_factory(TodoItem,
        form=TaskForm,
        can_order=True,
        can_delete=True, extra=2, max_num=10)
        
    if request.method == 'POST':
        instances = TaskFormSet(request.POST).save(commit=False)
        for instance in instances:
            instance.parent = goal
            instance.save()
    template_data = {
        'goal': goal,
        'formset': TaskFormSet(queryset=TodoItem.objects.filter(parent=goal)),
    }
    template_data.update(csrf(request))
    return render_to_response('todolist/view_goal.html', template_data)


def delete_goal(request):
    if request.method == 'POST':
        goal_id = request.POST.get('delete')
        goal = Goal.objects.get(pk=int(goal_id))
        goal.delete()
    redirect('goal-list')


def view_tasks(request):
    tasks = TodoItem.objects.filter(is_complete=False, is_current=True)
    if request.method == 'POST':
        print request.POST
        for task_id in request.POST.getlist('complete'):
            task = TodoItem.objects.get(pk=int(task_id))
            task.is_complete = True
            task.save()
    template_data = {
        'tasks': tasks
    }
    template_data.update(csrf(request))
    return render_to_response('todolist/view_tasks.html', template_data)

