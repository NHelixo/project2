from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from app.models import Task, Comment
from .models import Task
from django.utils import timezone


class TaskListView(ListView):
    model = Task
    template_name = "app/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        queryset = Task.objects.all()

        status = self.request.GET.get("status")
        if status == "in_progress":
            queryset = queryset.filter(status="in_progress")
        elif status == "done":
            queryset = queryset.filter(status="done")
        elif status == "overdue":
            queryset = queryset.filter(deadline__lt=timezone.now(), status__in=["todo", "in_progress"])

        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        priority_order = {
            'high': 1,
            'medium': 2,
            'low': 3
        }
        queryset = sorted(
            queryset,
            key=lambda t: (priority_order.get(t.priority, 99), t.deadline)
        )

        return queryset

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

class TaskDetailView(DetailView):
    model = Task
    template_name = "app/task_info.html"
    context_object_name = "task"

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "app/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def test_func(self):
        task = self.get_object()
        return task.owner == self.request.user
