from django.urls import path
from userauth.urls import app_name
from . import views

app_name = 'community'

urlpatterns = [
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('join-group/', views.join_group, name='join_group'),
]
