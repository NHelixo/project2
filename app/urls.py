from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskDeleteView


urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("/addtask", TaskCreateView.as_view(), name="task"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]