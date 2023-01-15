from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View, generic
from django.db.models import Q

from .models import CustomUser, Office, News, ProductsInOffice
# Create your views here.


class CustomUserView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    '''Класс-view отображения информации о пользователе'''
    permission_required = 'mtssite.view_customuser'
    model = CustomUser

    def get_context_data(self, *args, **kwargs):
        '''Функция переопределяет родительскую и возвращает context с информацией о пользователе'''
        context = super(CustomUserView, self).get_context_data(*args, **kwargs)
        context['userinfo'] = CustomUser.objects.filter(pk=self.object.pk)
        print(context)
        return context

# вывод списка новостей
class NewsListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    '''Класс-view отображения списка из пяти последних новостей'''
    permission_required = 'mtssite.view_news'
    model = News
    template_name = 'news_list.html'
    
    def get_queryset(self):
        '''Функция возвращает список из пяти последних элементов'''
        return News.objects.order_by('-publish_date')[:5]


# отображения списка магазинов
class OfficeListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    '''Класс-view отображения списка всех офисов'''
    permission_required = 'mtssite.view_office'
    model = Office
    template_name = 'office_list.html'

    def get_queryset(self):
        '''Функция возвращает список офисов'''
        return Office.objects.all()


# страница вывода детализации по магазину
class OfficeDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    '''Класс-view отображения выбранного офиса'''
    permission_required = ['mtssite.view_office', 'mtssite.view_productsinoffice']
    login_url = ''
    model = Office

    def get_context_data(self, *args, **kwargs):
        '''Функция переопределяет родительскую и возвращает context с информацией об офисе'''
        context = super(OfficeDetailView, self).get_context_data(*args, **kwargs)
        context['office_products'] = ProductsInOffice.objects.filter(office_id=self.object)
        print(context)
        return context


class SearchResultsView(LoginRequiredMixin, generic.ListView):
    login_url = ''
    model = Office
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("search_input")
        object_list = Office.objects.filter(
            Q(officename__icontains=query) | Q(officeaddress__icontains=query)
        )
        return object_list

# Вывод логин страницы
def authpage(request):
    template = loader.get_template('authpage.html')
    return HttpResponse(template.render({}, request))

# Аутентификация
def authuser(request):
    fusername = request.POST['fusername']
    fpassword = request.POST['fpassword']
    user = authenticate(request, username=fusername, password=fpassword)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('news-list'))
    else:
        return HttpResponseRedirect(reverse('authpage'))

# Функция выхода из профиля
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('authpage'))