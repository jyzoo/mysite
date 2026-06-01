from gc import get_objects
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import NewsForm
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    sucess_url = reverse_lazy('home')


class View_News(DetailView):
    model = News
    context_object_name = 'news_item'


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    #extra_context = {'titlel: 'Главная'}

def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
    return context

class NewsByCategory(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = False

def get_queryset(self):
    return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

class CategoryList(ListView):
    model = Category
    template_name = 'catalog/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список категорий'
        return context

def index(request):
    news = News.objects.all()

    context = {
        'news': news,

        'title': 'Список новостей'
    }
    return render(request, template_name='news/index.html', context=context)
    res = '<h1>Список новостей</h1>'
    for item in news:
        res += f'<div>\n<p>{item.title}</p>\n<p>{item.content}</p>\n</div>'
    return HttpResponse(res)


def get_category(request, category_id):
    news=News.objects.filter(category_id=category_id)

    category=Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})

def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)

    context = {
        'news_item': news_item
    }

    return render(request,
                  'news/view_news.html',
                  context=context)

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            news = form.save()
            return redirect(news)

    else:
        form = NewsForm()

    return render(
        request,
        'news/add_news.html',
        {'form': form}
    )



    return render(request, 'news/view_news.html', {'news_item': news_item})

def add_comment(request):
    success = False

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            success = True
            form = CommentForm()  # очистить форму

    else:
        form = CommentForm()

    return render(
        request,
        'news/add_comment.html',
        {
            'form': form,
            'success': success
        }
    )

