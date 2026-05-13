from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200) # عنوان المهمة
    completed = models.BooleanField(default=False) # هل اكتملت؟
    created_at = models.DateTimeField(auto_now_add=True) # تاريخ الإنشاء

    def __str__(self):
        return self.title