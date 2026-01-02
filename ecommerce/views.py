from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'home.html')

def cakes(request):
    return render(request,'cakes.html')

def puddings(request):
    return render(request,'puddings.html')

def desserts(request):
    return render(request,'desserts.html')

def dryfruits(request):
    return render(request,'dryfruits.html')

def sugarfree(request):
    return render(request,'sugarfree.html')

def gift(request):
    return render(request,'gift.html')