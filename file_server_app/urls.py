from django.http import HttpResponse
from django.urls import path

from file_server_app import views

urlpatterns = [
    path('', views.ContentList.as_view()),
    path('<path:path>', views.ContentList.as_view()),
]
