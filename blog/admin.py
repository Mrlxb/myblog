from django.contrib import admin
from .models import BlogPost, ArticleColumn
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(ArticleColumn)
