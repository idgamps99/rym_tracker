from django.urls import path
from . import views

app_name = "visits"
urlpatterns = [
    path("unique/", views.UniqueVisitsView.as_view())
]
