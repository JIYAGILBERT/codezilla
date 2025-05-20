# capp/admin.py
from django.contrib import admin
from .models import Category, Question, Option

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Option)