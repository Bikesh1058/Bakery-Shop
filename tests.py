from django.http import HttpResponse
from django.shortcuts import render 
from django.core.files.storage import FileSystemStorage

def homepage(request):
    return render(request, 'homepage.html')