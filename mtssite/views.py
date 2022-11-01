from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.db.models import Q

from .models import Office, News
# Create your views here.

# вывод списка новостей
class NewsListView(LoginRequiredMixin, generic.ListView):
    model = News
    template_name = 'news_list.html'
    
    def get_queryset(self):
        return News.objects.order_by('-publish_date')[:5]


# отображения списка магазинов
class OfficeListView(LoginRequiredMixin, generic.ListView):
    model = Office
    template_name = 'office_list.html'

    def get_queryset(self):
        return Office.objects.all()


# страница вывода детализации по магазину
class OfficeDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = ''
    model = Office


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


# вывод страницы добавления офиса
@login_required
def addoffice(request):
    template = loader.get_template('office_add.html')
    return HttpResponse(template.render({}, request))


# добавить запись в бд
@login_required
def addrecord(request):
    oname = request.POST['officename']
    oaddress = request.POST['officeaddress']
    ohead = request.POST['officehead']
    otn = request.POST['officetnumber']
    office = Office(officename=oname, officeaddress=oaddress,
                    officehead=ohead, officeheadtnumber=otn)
    office.save()
    return HttpResponseRedirect(reverse('office-list'))

# удаление строки офиса из бд по id
@login_required
def deleterow(request, id):
    office = Office.objects.get(id=id)
    office.delete()
    return HttpResponseRedirect(reverse('office-list'))

# вывод страницы редактирования
@login_required
def updaterow(request, id):
    office = Office.objects.get(id=id)
    template = loader.get_template('office_update.html')
    context = {
        'office': office
    }
    return HttpResponse(template.render(context, request))

# изменение данных определенной строки в бд
@login_required
def updaterowrecord(request, id):
    oname = request.POST['officename']
    oaddress = request.POST['officeaddress']
    ohead = request.POST['officehead']
    otn = request.POST['officetnumber']
    office = Office.objects.get(id=id)
    office.officename = oname
    office.officeaddress = oaddress
    office.officehead = ohead
    office.officeheadtnumber = otn
    office.save()
    return HttpResponseRedirect(reverse('office-list'))

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

@login_required
def userprofile_view(request):
    template = loader.get_template('user-profile.html')
    return HttpResponse(template.render({}, request))