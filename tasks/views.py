from turtle import title
from django.shortcuts import redirect, render , get_object_or_404

# Create your views here.

from .models import Task
def task_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
    Tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': Tasks})

def task_delete(request, task_id):
    task =get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
def task_list(request):
    # 1. استقبال نص البحث أولاً
    search_query = request.GET.get('search', '')

    # 2. معالجة إضافة مهمة جديدة (POST)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        # بعد الإضافة، نعود للصفحة الرئيسية بدون فلاتر بحث
        return redirect('task_list')

    # 3. جلب المهام بناءً على البحث (GET)
    if search_query:
        # لاحظ هنا استخدمنا اسم متغير tasks (صغير) ليتناسب مع الـ Template
        tasks = Task.objects.filter(title__icontains=search_query).order_by('-created_at')
    else:
        tasks = Task.objects.all().order_by('-created_at')

    # 4. إرسال البيانات للـ Template
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks, 
        'search_query': search_query
    })
def task_update (request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_update.html', {'task': task})
    
