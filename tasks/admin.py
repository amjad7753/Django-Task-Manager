from django.contrib import admin
from .models import Task # استيراد موديل المهام

# تسجيل الموديل ليظهر في لوحة التحكم
admin.site.register(Task)