from django.urls import path

from . import views

app_name = "period_tracker"

urlpatterns = [
    path('', views.CycleDatesView.as_view(), name="cycle")
]
