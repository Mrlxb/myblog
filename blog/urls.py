from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog-list/', views.blog_list, name='blog-list'),
    path('article-detail/<int:id>', views.article_detail, name='article-detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-safe-delete/<int:id>', views.article_safe_delete, name='article_safe_delete'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]

