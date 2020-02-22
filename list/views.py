from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

def home_page(request):
    if request.method == 'POST':
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        return redirect('/')

    context = {'items' : Item.objects.all()}
    return render(request, 'list/home.html', context) 

