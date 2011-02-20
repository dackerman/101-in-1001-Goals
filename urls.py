from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
import todolist
import todolist.views
from todolist.models import Goal
from django.forms.models import modelformset_factory
from django.conf import settings


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^accounts/new/$', todolist.views.new_user, name='new-user'),
    (r'^$', todolist.views.list_goals),
    url(r'^goals/$', todolist.views.list_goals, name='goal-list'),
    url(r'^goal/(\d+)/$', todolist.views.view_goal, name='view-goal'),
    url(r'^goal/(\d+)/edit/$', todolist.views.edit_goal, name='edit-goal'),
    url(r'^goal/(\d+)/delete/$', todolist.views.delete_goal, name='delete-goal'),
    url(r'^tasks/$', todolist.views.view_tasks, name='view-tasks'),
    url(r'^categories/edit/$', todolist.views.update_categories, name='update-categories'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),
)
