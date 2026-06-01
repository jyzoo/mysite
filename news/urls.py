from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),

    path('category/<int:pk>/', NewsByCategory.as_view(extra_context={'title': 'Какой-то заголовок'}),
         name='category'),

    path('news/<int:pk>/',
         views.View_News.as_view(),
         name='view_news'),

    path('news/add-news-', CreateNews.as_view(), name='add_news'),

path(
    'add-comment/',
    views.add_comment,
    name='add_comment'
),

path('categories/', CategoryList.as_view(), name='categories'),
]