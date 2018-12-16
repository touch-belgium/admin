from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Tag
from .serializers import UserSerializer, PostSerializer, TagSerializer
# Create your views here.


def index(request):
    return render(request, 'index.html')


def news(request):
    posts = Post.objects.order_by('-pk')
    paginator = Paginator(posts, 5)

    page = request.GET.get('page')
    first_posts = paginator.get_page(page)
    context = {"posts": first_posts}
    return render(request, 'news.html', context)


def new(request, id, slug=""):
    return render(request, 'new.html', {"post": Post.objects.get(pk=id)})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        number = self.request.query_params.get('number', None)
        if number:
            queryset = queryset[:int(number)]

        return queryset


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
