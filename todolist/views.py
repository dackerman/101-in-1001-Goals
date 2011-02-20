from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from todolist.models import Goal
from todolist.models import TodoItem
from todolist.models import Tag
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

    goals = Goal.objects.all()

    template_data = {
        'goals': goals,
        'goalform': GoalForm(),
    }
    return render(request, 'todolist/list_goals.html', template_data)
    
@login_required
def view_tag(request, tag_name):
    tags = Tag.objects.all().filter(name=tag_name)
    goals = []
    for tag in tags:
        goals.append(tag.goal)
    return render(request, 'todolist/view_tag.html', {'goals': goals, 'tag': tag_name})

@login_required
def edit_goal(request, goal_id):
    if request.method == 'POST':
        goal = Goal.objects.get(pk=goal_id)
        goalform = GoalForm(request.POST, instance=goal)
        goalform.save()
        
    return redirect('view-goal', goal_id)

@login_required
def view_goal(request, goal_id):
    goal = Goal.objects.get(pk=goal_id)
    goalform = GoalForm(instance=goal)
    TagFormset = inlineformset_factory(Goal, Tag)
    tags = TagFormset(instance=goal)
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
        'tagformset': tags,
        'formset': TaskFormSet(queryset=TodoItem.objects.filter(parent=goal)),
    }
    return render(request, 'todolist/view_goal.html', template_data)


@login_required
def delete_goal(request):
    if request.method == 'POST':
        goal_id = request.POST.get('delete')
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
    
@login_required
def update_tags(request, goal_id):
    if(request.method == 'POST'):
        goal = Goal.objects.get(pk=goal_id)
        TagFormset = inlineformset_factory(Goal, Tag)
        tags = TagFormset(request.POST, instance=goal)
        tags.save()
    return redirect('view-goal', goal_id)

