from gc import get_objects

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import NewsForm, ContactForm
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import Mymixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator



class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    sucess_url = reverse_lazy('home')
    login_url = '/admin/'


class View_News(DetailView):
    model = News
    context_object_name = 'news_item'


class HomeNews(Mymixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    paginate_by = 5
    #extra_context = {'titlel: 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(Mymixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['pk']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['pk'], is_published=True).select_related('category')



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

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ContactForm()

    return render(request,
                  'news/contact.html',
                  {'form': form})

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

    return render(request, 'news/add_comment.html', {'form': form})

def home(request):
    news = News.objects.filter(
            is_published=True
    ).select_related('category')

    paginator = Paginator(news, 5)

    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'news': page_objects.object_list,
        'page_obj': page_objects,
        'title': 'Главная страница'
    }

    return render(request, 'news/home_news_list.html', context)

