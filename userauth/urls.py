from django.urls import path
from .views import signup_view, login_view, logout_view, home_view
from . import views

app_name = 'userauth'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('profile/glucose', views.glucose_log_view, name='glucose_log'),
    path('profile/glucose/delete/<int:glucose_id>', views.glucose_log_delete, name='glucose_log_delete'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
]
