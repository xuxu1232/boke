from django.http import HttpResponse
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator

# def test(request):
#     return HttpResponse('testyemian')

def about(request):
    return render(request,'about.html',locals())

def index(request):
    article = Article.objects.order_by('-date')[:6]
    recommend_article = Article.objects.filter(recommend=1)[:7]
    click_article = Article.objects.order_by('-click')[:12]

    return render(request,'index.html',locals())

def listpic(request):
    return render(request,'listpic.html',locals())

def newslistpic(request,page=1):
    page = int(page)
    article = Article.objects.order_by('-date')
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


def reqtest(request):
    # print(request)
    # print(dir(request))
    # meta = request.META
    # for key in meta:
    #     print(key)
    # print(meta.get('OS'))
    # print(meta.get('HTTP_HOST'))
    # print(meta.get('HTTP_USER_AGENT'))
    # print(meta.get('HTTP_REFERER'))

    # print(request.COOKIES)
    # print(request.FILES)
    # print(request.GET)
    # print(request.POST)
    # print(request.scheme)
    # print('--------------')
    # print(request.path)
    # print('---------------')
    # print(request.method)
    # print('-----------------')
    # print(request.body)
    return HttpResponse('姓名：%s,年龄%s'%(request.POST.get('name'),request.POST.get('age')))

def formtest(request):
    # # 获取输入的数据
    # search = request.GET
    # data = search.get('search')
    # # 在数据库查询数据
    # article = Article.objects.filter(title__contains=data).all()
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    return render(request,'formtest.html',locals())
import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
from Article.forms import Register
def register(request):
    register_form = Register()
    error = ''
    if request.method == 'POST':
        data = Register(request.POST)
        if data.is_valid():
            clean_data = data.cleaned_data
            username = clean_data.get('name')
            password = clean_data.get('password')
            user = User()
            user.name = username
            user.password = setPassword(password)
            user.save()
            error = '添加数据成功'
        else:
            error = data.errors
            print(error)


    return render(request,'register.html',locals())

def jiaoyan(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if password:
        password = setPassword(password)
        user = User.objects.filter(name=username).first()
        content = '密码不正确，登录失败'
        if password == user.password:
            content = '登陆成功'





    return render(request,'jiaoyan.html',locals())

