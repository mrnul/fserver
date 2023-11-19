from django.urls import path

from file_server_app import views

urlpatterns = [
    path('', views.drives),
    path('<path:path>', views.content),
]
