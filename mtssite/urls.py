from django.urls import path
from . import views
urlpatterns = [
    path('', views.authpage, name='authpage'),
    path('search/', views.SearchResultsView.as_view(), name='search_result'),
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('profile/<int:pk>', views.CustomUserView.as_view(), name='user-profile-detail'),
    path('authuser/', views.authuser, name='authuser'),
    path('logout/', views.logout_view, name='logout_view'),
    path('office/', views.OfficeListView.as_view(), name='office-list'),
    path('office/<int:pk>', views.OfficeDetailView.as_view(), name='office-detail'),
]