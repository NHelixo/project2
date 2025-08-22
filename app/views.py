from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from app.models import Task, Comment

class TaskListView(ListView):
    model = Task
    template_name = "app/index.html"
    context_object_name = "task_list"

class TaskCreateView(CreateView):
    model = Task
    template_name = 'app/add_task.html'
    fields = ()
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.text = self.request.POST.get('text')
        form.instance.priority = self.request.POST.get('priority')
        form.instance.deadline = self.request.POST.get('deadline')
        form.instance.owner = self.request.user
        return super().form_valid(form)
