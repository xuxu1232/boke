# from django.http import HttpResponse
from django.shortcuts import render
# def test(request):
#     return HttpResponse('testyemian')

def about(request):
    return render(request,'about.html',locals())

def index(request):
    return render(request,'index.html',locals())

def listpic(request):
    return render(request,'listpic.html',locals())

def newslistpic(request):
    return render(request,'newslistpic.html',locals())

def base(request):
    return render(request,'base.html',locals())

