from django.urls import path
from . import views
urlpatterns = [
    path('', views.authpage, name='authpage'),
    path('search/', views.SearchResultsView.as_view(), name='search_result'),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('profile/', views.userprofile_view, name='user-profile'),
    path('authuser/', views.authuser, name='authuser'),
    path('logout/', views.logout_view, name='logout_view'),
    path('office/', views.OfficeListView.as_view(), name='office-list'),
    path('office/<int:pk>', views.OfficeDetailView.as_view(), name='office-detail'),
    path("office/update/<int:id>", views.updaterow, name='updaterow'),
    path("office/delete/<int:id>", views.deleterow, name='deleterow'),
    path("office/addoffice/", views.addoffice, name='addoffice'),
    path("office/addoffice/addrecord/", views.addrecord, name='addrecord'),
    path("office/update/updaterow/<int:id>", views.updaterowrecord, name='updaterowrecord'),
]