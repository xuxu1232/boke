from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator

# def test(request):
#     return HttpResponse('testyemian')


def loginValid(func):
    def inner(request,*args,**kwargs):
        email = request.COOKIES.get('email')
        email_session = request.session.get('email')
        if email and email_session:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner


@loginValid
def about(request):
    return render(request,'about.html',locals())


@loginValid
def index(request,page=1):
    page = int(page)
    article = Article.objects.order_by('-date')
    paginator = Paginator(article,6)
    page_obj = paginator.page(page)

    current_page = page_obj.number
    start = current_page - 3
    end = current_page + 2
    if start < 0:
        start = 0
        end = 5
    if end > paginator.num_pages:
        end = paginator.num_pages
        start = end-5
    page_range = paginator.page_range[start:end]
    recommend_article = Article.objects.filter(recommend=1)[:7]
    click_article = Article.objects.order_by('-click')[:12]

    return render(request,'index.html',locals())


def listpic(request):
    return render(request,'listpic.html',locals())

def newslistpic(request,type,page=1):
    page = int(page)
    type = Type.objects.filter(name=type).first()
    article = type.article_set.order_by('-date')
    paginator = Paginator(article,6)
    page_obj = paginator.page(page)
    # 使五页为一周期
    # 获取当前页的页码
    current_page = page_obj.number
    # 第一个页数
    start = current_page-3
    if start<1:
        start = 0
    # 最后一个页数
    end = current_page+2
    if end>paginator.num_pages:
        end = paginator.num_pages

    if start == 0:
        end = 5
    if end == paginator.num_pages:
        start = paginator.num_pages-5
    page_range = paginator.page_range[start:end]
    return render(request,'newslistpic.html',locals())

def base(request):
    return render(request,'base.html',locals())


def articledetails(request,id):
    id = int(id)
    article = Article.objects.get(id = id)
    return render(request,'articledetails.html',locals())

def adddata(request):
    for i in range(100):
        article = Article()
        article.title = 'title_%s'%i
        article.content = 'content_%s'%i
        article.description = 'description_%s'%i
        article.author = Author.objects.get(id=1)
        article.save()
        article.type.add(Type.objects.get(id=1))
    return HttpResponse('增加数据')
def fytest(request):
    article = Article.objects.all().order_by('-date')
    # 使用Paginator进行分页时，要进行排序
    # 第一个参数为总数据，第二个参数为每页多少个数据
    paginator = Paginator(article,5)

    # count:总共多少页
    # print(paginator.count)

    # page_range:页码取值范围
    # print(paginator.page_range)

    # num_pages:最大页码数
    # print(paginator.num_pages)

    # 定义某一页的对象，包含指定页的数据
    pag_obj = paginator.page(2)
    for one in pag_obj:
        print(one.title)

    # number:返回当前页的页码
    # print(pag_obj.number)

    # has_next：判断是否有下一页：True/False
    # print(pag_obj.has_next())

    # has_previous：判断是否有前一页：True/False
    # print(pag_obj.has_previous())

    # has_other_pages：判断是否有其他页：True/False
    # print(pag_obj.has_other_pages())

    # next_page_number：下一页的页码
    # print(pag_obj.next_page_number())

    # previous_page_number：上一页的页码
    # print(pag_obj.previous_page_number())

    return HttpResponse('分页测试')

import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def register(request):
    email = request.POST.get('email')
    password = request.POST.get("password")
    password2 = request.POST.get('password2')
    if email:
        user = Author.objects.filter(email=email).first()
        if user:
            error = '用户已存在'
        else:
            if password and password2 and password==password2:
                user = Author()
                user.email = email
                user.password = setPassword(password)
                user.name = email
                user.save()
                return HttpResponseRedirect('/login/')
            else:
                error = '密码有误'
    else:
        error = '邮箱不能为空'
    return render(request,'register.html',locals())

def login(request):
    # 获取登录数据
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Author.objects.filter(email=email,password=setPassword(password)).first()
        print(user)
        if user:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('email',email)
            request.session['email'] = email
            return response
        else:
            error = '用户不存在'
    return render(request,'login.html',locals())

def logout(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('email')
    del request.session['email']
    return response


# 添加博文
@loginValid
def addarticle(request):
    type = Type.objects.all()
    return render(request,'addarticle.html',locals())
@loginValid
def add_article(request):
    if request.method == 'POST':
        email = request.COOKIES.get('email')
        title = request.POST.get('title')
        print(title)
        content = request.POST.get('content')
        description = request.POST.get('description')
        type = request.POST.get('article_type')
        print(type)
        article = Article()
        article.title = title
        article.content = content
        article.description = description
        article.author = Author.objects.filter(email=email).first()
        if request.FILES.get('picture'):
            article.picture = request.FILES.get('picture')
        article.save()
        article = Article.objects.filter(title__contains=title).order_by('-date').first()
        type = Type.objects.get(id=type)
        article.type.add(type)
        article.save()
    return render(request,'add_article.html',locals())

def searcharticle(request):
    title = request.GET.get('keyboard')
    article = Article.objects.filter(title__contains=title)
    return render(request,'search_article.html',locals())
