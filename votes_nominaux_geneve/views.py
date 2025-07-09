from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def selection_rgse(request):
    # get the X
    # get the chapters
    return render(request, "selection-rgse.html")
