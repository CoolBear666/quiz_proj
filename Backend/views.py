from django.http import request
from django.shortcuts import render

def first(request):
    return render(request, 'first.html')