from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [

    path('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    # path('delete-comment/<int:comment_id>', views.delete_comment, name='delete_commentete_comment')
    # 已有代码，处理一级回复
    path('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    # 新增代码，处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]
