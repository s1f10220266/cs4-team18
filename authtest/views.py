from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from .forms import TodoItemForm
from django.http import Http404

# Create your views here.

def home(request):
    return render(request, 'authtest/home.html', {})

def withoutLogin(request):
    #djangoのセッションを用意、リロードすると消える
    todo_items = request.session.get('todo_items', [])

    if request.method == 'POST':
        if 'add_todo' in request.POST:
            # ToDo作成
            new_todo = {
                'title': request.POST.get('title', ''),
                'due_date': request.POST.get('due_date', ''),
                'notes': request.POST.get('notes', ''),
            }
            # ToDo項追加
            todo_items.append(new_todo)
            request.session['todo_items'] = todo_items
            return redirect(withoutLogin)

        if 'delete_todo' in request.POST:
            # 削除するToDoのインデックスを取得
            delete_index = int(request.POST.get('delete_todo'))
            # ToDoを削除
            del todo_items[delete_index]
            request.session['todo_items'] = todo_items
            return redirect(withoutLogin)

    return render(request, 'authtest/withoutLogin.html', {'todo_items': todo_items})


@login_required
def todo_list(request):
    todo_items = TodoItem.objects.filter(user=request.user)
    form = TodoItemForm()

    if request.method == 'POST':
        form = TodoItemForm(request.POST)

        if 'add_todo' in request.POST: #追加
            if form.is_valid():
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                return redirect('todo_list')

        if 'delete_todo' in request.POST: #削除
            todo_id_to_delete = request.POST.get('delete_todo')
            todo_to_delete = get_object_or_404(TodoItem, id=todo_id_to_delete, user=request.user)
            todo_to_delete.delete()

    return render(request, 'authtest/todo_list.html', {'todo_items': todo_items, 'form': form})

def detail(request, todo_id):
    try:
        todo = TodoItem.objects.get(pk=todo_id)
    except TodoItem.DoesNotExist:
        raise Http404("This Todo is over.")
    return render(request, 'authtest/detail.html', {'todo': todo})

def edit(request, todo_id):
    try:
        todo = TodoItem.objects.get(pk=todo_id)
    except TodoItem.DoesNotExist:
        raise Http404("This Todo is over.")
    
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo)
        
        if 'edit_todo' in request.POST:
            if form.is_valid():
                edited_todo = form.save(commit=False)
                if request.POST['due_date'] == None:
                    edited_todo.due_date = todo.due_date
                edited_todo.save()
                return redirect(edit, todo_id)
    else:
        form = TodoItemForm(instance=todo)
    return render(request, 'authtest/edit.html', {'todo': todo})