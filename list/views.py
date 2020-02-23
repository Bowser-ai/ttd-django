from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

def home_page(request):

    return render(request, 'list/home.html') 

def list_view(request):
    context = {'items' : Item.objects.all()}
    return render(request, 'list/list.html', context) 

def new_list(request):
    Item.objects.create(text=request.POST['item_text'], list=List.objects.create())
    return redirect('/lists/the-only-list-in-the-world/')

