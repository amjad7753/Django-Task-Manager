from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Task

from django.db import IntegrityError # استيراد مكتبة الخطأ

def task_list(request):
    # استقبال وإضافة المهمة الجديدة مع إرسال الرسائل التنبيهية
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            try:
                Task.objects.create(title=title)
                messages.success(request, '🎉 تم إضافة المهمة بنجاح!') # رسالة نجاح
            except IntegrityError:
                messages.error(request, '⚠️ هذه المهمة موجودة بالفعل في قائمتك!') # رسالة خطأ عند التكرار
            
            return redirect('task_list')

    # كود العرض والبحث والإحصائيات كما هو
    search_query = request.GET.get('liveSearch', '')
    if search_query:
        tasks = Task.objects.filter(title__icontains=search_query)
    else:
        tasks = Task.objects.all()

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    remaining_tasks = Task.objects.filter(completed=False).count()
    
    if total_tasks > 0:
        progress_percentage = (completed_tasks / total_tasks) * 100
    else:
        progress_percentage = 0

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'remaining_tasks': remaining_tasks,
        'progress_percentage': progress_percentage,
        'search_query': search_query,
    }
    return render(request, 'tasks/task_list.html', context)
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


def task_update(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':

        title = request.POST.get('title')

        if title:

            # منع التكرار أثناء التعديل
            if Task.objects.filter(title=title).exclude(id=task.id).exists():
                messages.error(request, 'المهمة موجودة مسبقاً')
            else:
                task.title = title
                task.save()
                messages.success(request, 'تم تعديل المهمة')

        return redirect('task_list')

    return render(request, 'tasks/task_update.html', {
        'task': task
    })