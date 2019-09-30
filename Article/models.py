from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
GENDER_LIST = (
    (1,'男'),
    (2,'女'),
)
class Author(models.Model):
    name = models.CharField(max_length=32,verbose_name='作者姓名')
    age = models.IntegerField(null=True,verbose_name='作者年龄')
    gender = models.IntegerField(choices=GENDER_LIST,verbose_name='作者性别',default=1)
    email = models.EmailField(max_length=32,verbose_name='作者邮箱')
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'
        verbose_name = 'Author'
        verbose_name_plural = verbose_name

class Type(models.Model):
    name = models.CharField(max_length=32,verbose_name='类型名')
    description = models.TextField(verbose_name='类型描述')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'type'
        verbose_name = 'Type'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=32,verbose_name='标题')
    date = models.DateField(auto_now=True,verbose_name='发布日期')
    # content = models.TextField(verbose_name='文章内容')
    content = RichTextField()
    # description = models.TextField(verbose_name='文章描述')
    description = RichTextField()
    picture = models.ImageField(upload_to='images')
    recommend = models.IntegerField(default=0,verbose_name='推荐')  #1表示推荐
    click = models.IntegerField(default=0,verbose_name='点击率')
    author = models.ForeignKey(to=Author,to_field='id',on_delete=models.SET_DEFAULT,default=1,verbose_name='文章作者')
    type = models.ManyToManyField(to=Type,verbose_name='文章类型')

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'article'
        verbose_name = 'Article'
        verbose_name_plural = verbose_name

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        db_table = 'user'