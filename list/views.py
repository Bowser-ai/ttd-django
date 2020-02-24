from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

def home_page(request):

    return render(request, 'list/home.html') 

def list_view(request, list_id):
    list_ = List.objects.get(id=list_id)
    context = {'list' : list_}
    return render(request, 'list/list.html', context) 

def new_list(request):
    item = Item.objects.create(text=request.POST['item_text'], list=List.objects.create())
    return redirect(f'/lists/{item.list.id}/')

def add_item(request, list_id):
    Item.objects.create(text=request.POST['item_text'],
                        list=List.objects.get(id=list_id))
    return redirect(f'/lists/{list_id}/')

