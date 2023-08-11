from django.shortcuts import render, redirect
from django.http import HttpResponse

from comment.forms import CommentForm
from .models import BlogPost, ArticleColumn
from comment.models import Comment
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
# 视图函数
def blog_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = BlogPost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        ).order_by('-total_views')
    else:
        search = ''
    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
        # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
        # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    blogs = paginator.get_page(page)
    context = {'blogs': blogs, 'order': order, 'search': search, 'column': column, 'tag': tag}
    return render(request, "blog/list.html", context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = BlogPost.objects.get(id=id)
    # 引入评论表单
    comment_form = CommentForm()
    # 取出文章对应评论
    comments = Comment.objects.filter(article=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    # 需要传递给模板的对象
    context = {'article': article,
               'toc': md.toc,
               'comments': comments,
               'comment_form': comment_form
               }

    # 载入模板，并返回context对象
    return render(request, 'blog/detail.html', context)


# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("blog:blog-list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, "columns": columns}
        # 返回模板
        return render(request, 'blog/create.html', context)


def article_safe_delete(request, id):
    if request.method == 'POST':
        article = BlogPost.objects.get(id=id)
        article.delete()
        return redirect("blog:blog-list")
    else:
        return HttpResponse('仅允许post请求')


# 提醒用户登录
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = BlogPost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            # 新增的代码
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("blog:article-detail", id=id)
        else:
            return HttpResponse('表单内容有误，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'blog/update.html', context)
