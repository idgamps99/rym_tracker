from django.urls import path
from . import views

app_name = "visits"
urlpatterns = [
    path("record", views.RecordVisitView.as_view())
]
