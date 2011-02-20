from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from todolist.models import *
import datetime
from django import forms
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def render(request, template, data):
    data.update({'username': request.user.username})
    data.update(csrf(request))
    return render_to_response(template, data)

class GoalForm(ModelForm):
    def next_year():
        return datetime.date.today() + datetime.timedelta(365)
        
    deadline = forms.DateField(label="Due", initial=next_year)
    class Meta:
        model = Goal
        widgets = {
            'name': forms.TextInput(attrs={'size':'40'})
        }

class TaskForm(ModelForm):
    class Meta:
        model = TodoItem
        exclude = ('parent',)
        widgets = {
            'name': forms.TextInput(attrs={'size':'70'})
        }
        
def new_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
        user.save()
    return redirect('login')
    
        
@login_required
def list_goals(request):
    if request.method == 'POST':
        goal = GoalForm(request.POST)
        goal.save()

    categories = Category.objects.all()
    goals_without_categories = Goal.objects.all().filter(category=None)

    template_data = {
        'categories': categories,
        'goals_without_categories': goals_without_categories,
        'goalform': GoalForm(),
        'goal_length': Goal.objects.all().count(),
    }
    return render(request, 'todolist/list_goals.html', template_data)

@login_required
def edit_goal(request, goal_id):
    if request.method == 'POST':
        goal = Goal.objects.get(pk=goal_id)
        goalform = GoalForm(request.POST, instance=goal)
        goalform.save()
        
    return redirect('view-goal', goal_id)

@login_required
def update_categories(request):
    CategoryFormSet = modelformset_factory(Category, can_delete=True)
    if request.method == 'POST':
        categories = CategoryFormSet(request.POST)
        categories.save()

    template_data = {
        'formset': CategoryFormSet()
    }
    return render(request, 'todolist/edit_categories.html', template_data)

@login_required
def view_goal(request, goal_id):
    goal = Goal.objects.get(pk=goal_id)
    goalform = GoalForm(instance=goal)
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
        'goalform': goalform,
        'formset': TaskFormSet(queryset=TodoItem.objects.filter(parent=goal)),
    }
    return render(request, 'todolist/view_goal.html', template_data)


@login_required
def delete_goal(request, goal_id):
    if request.method == 'POST':
        goal = Goal.objects.get(pk=int(goal_id))
        goal.delete()
    return redirect('goal-list')


@login_required
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
    return render(request, 'todolist/view_tasks.html', template_data)


