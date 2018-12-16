from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('where', views.index, name='where'),
    path('competitions', views.index, name='competitions'),
    path('rules', views.index, name='rules'),
    path('news', views.news, name='news'),
    path('news/<int:id>/', views.new, name='new'),
    path('news/<int:id>/<slug:slug>/', views.new, name='new')
]
