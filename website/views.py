from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Tag, Venue, Team, Competition, Match
from .serializers import UserSerializer, PostSerializer, TagSerializer, TeamSerializer, CompetitionSerializer, MatchSerializer, VenueSerializer
# Create your views here.


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


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
