from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from app.models import Task, Comment
from .models import Task
from django.utils import timezone
from django.views import View


class TaskListView(ListView):
    model = Task
    template_name = "app/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        queryset = Task.objects.all()

        status = self.request.GET.get("status")
        if status == "В процесі":
            queryset = queryset.filter(status="В процесі")
        elif status == "Виконані":
            queryset = queryset.filter(status="Виконані")
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

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "app/task_info.html"
    context_object_name = "task"
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user == self.object.owner:
            text = request.POST.get('task_text', '').strip()
            status = request.POST.get('status', '').strip()
            priority = request.POST.get('priority', '').strip()
            deadline = request.POST.get('deadline', '').strip()

            if text:
                self.object.text = text
            if status:
                self.object.status = status
            if priority:
                self.object.priority = priority
            if deadline:
                self.object.deadline = deadline

            self.object.save()

        return redirect('task_detail', pk=self.object.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(task=self.object).order_by("-add_datetime")
        return context

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "app/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def test_func(self):
        task = self.get_object()
        return task.owner == self.request.user
    
class AddCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)

        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(
                task=task,
                owner=request.user,
                text=text,
                add_datetime=timezone.now()
            )

        return redirect("task_detail", pk=task.pk)
