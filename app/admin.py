from django.contrib import admin
from app.models import Task, Comment

admin.site.register([Task, Comment])
