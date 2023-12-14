from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from .forms import TodoItemForm

# Create your views here.

def home(request):
    return render(request, 'authtest/home.html', {})

@login_required
def todo_list(request):
    todo_items = TodoItem.objects.filter(user=request.user)
    form = TodoItemForm()

    if request.method == 'POST':
        form = TodoItemForm(request.POST)

        if 'add_todo' in request.POST:  # アイテムの追加
            if form.is_valid():
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                return redirect('todo_list')

        if 'delete_todo' in request.POST:  # アイテムの削除
            todo_id_to_delete = request.POST.get('delete_todo')
            todo_to_delete = get_object_or_404(TodoItem, id=todo_id_to_delete, user=request.user)
            todo_to_delete.delete()

    return render(request, 'authtest/todo_list.html', {'todo_items': todo_items, 'form': form})