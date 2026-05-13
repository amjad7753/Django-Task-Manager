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
    search_query = request.GET.get('search', '')
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
    if search_query:
        Tasks = Task.objects.filter(title__icontains=search_query).order_by('-created_at')
    else:
        Tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': Tasks, 'search_query': search_query})