from django.urls import path
from . import views
from .views import add_news

urlpatterns = [
    path('', views.index, name='home'),

    path('category/<int:category_id>/',
         views.get_category,
         name='category'),

    path('news/<int:news_id>/',
         views.view_news,
         name='view_news'),

    path('news/add-news-', add_news, name='add_news'),

path(
    'add-comment/',
    views.add_comment,
    name='add_comment'
),
]