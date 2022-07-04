from django.urls import path

from . import views

urlpatterns = [

  path('task/upload/<str:filename>', views.TaskUploadView.as_view(), name='task_upload'),
  path('task/<str:task_id>/', views.TaskView.as_view(), name='task'),
]