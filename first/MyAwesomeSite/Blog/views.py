from django.shortcuts import render
from .models import BlogModels
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def first(request,blog_name):
    return render(request,"HTML Files/index.html")
