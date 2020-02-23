from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

def home_page(request):
    if request.method == 'POST':
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        return redirect('/lists/the-only-list-in-the-world/')

    return render(request, 'list/home.html') 

def list_view(request):
    context = {'items' : Item.objects.all()}
    return render(request, 'list/list.html', context) 

