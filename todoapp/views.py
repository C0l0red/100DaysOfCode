from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import TodoListItem, TodoCategory
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages import constants as mess

MESSAGE_TAGS = {
    mess.ERROR: 'error',
    50: 'error',
}
# Create your views here.
def todoappView(request):
    return render(request, 'todolist.html')

def todoappView(request, category_name=None):
    disabled = "disabled"
    all_todo_items = TodoListItem.objects.all()
    categories = TodoCategory.objects.all()
    category = None
    if category_name:
        category = TodoCategory.objects.filter(name=category_name)[0]
        disabled = ""
    print()
    return render(request, 'todolist.html',
    {'all_items':all_todo_items, "category":category, "disabled":disabled, "categories": categories}) 

def addTodoView(request, next):
    content, category_name, username = request.POST['content'], request.POST['category_name'], request.POST['username']
    category = TodoCategory.objects.filter(name=category_name)[0]
    new_item = TodoListItem(content = content, category=category, username=username)
    new_item.save()
    return HttpResponseRedirect('/todoapp/'+next) 

def deleteTodoView(request, id, next):
    item = TodoListItem.objects.get(id= id)

    if item.username != request.POST['delete-username']:
        messages.add_message(request, mess.ERROR, 'Wrong Username.\nPlease enter the username used to create the Todo')
        return HttpResponseRedirect('/todoapp/'+next)
    item.delete()
    return HttpResponseRedirect('/todoapp/'+next) 

@csrf_exempt
def addCategory(request):
    category_name = request.POST['name']
    print(TodoCategory.objects.filter(name=category_name))
    if not TodoCategory.objects.filter(name=category_name):
        new_category = TodoCategory(name=category_name)
        new_category.save()
        return JsonResponse({'success': "saved", "name": new_category.name})
    else:
        return JsonResponse({"error":"exists"})
    