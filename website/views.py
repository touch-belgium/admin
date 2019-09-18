from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Tag, Venue, Team, Competition, Match, TBMember, \
    Event, File, Link
from .serializers import UserSerializer, PostSerializer, TagSerializer, \
    TeamSerializer, CompetitionSerializer, MatchSerializer, VenueSerializer,\
    TBMemberSerializer, EventSerializer, FileSerializer, LinkSerializer
# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=False)
    def recent(self, request):
        recent_users = User.objects.all().order_by('date_joined')
        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    RECENT = 4

    @action(detail=False)
    def recent(self, request):
        """Limits the response to 4 posts, useful for not having to send the
        whole blog to the landing page. Called like: 'posts/recent' in
        the API

        """
        recent_posts = self.queryset[:self.RECENT]
        page = self.paginate_queryset(recent_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    paginator = None


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    paginator = None

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchCompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MatchSerializer

    def get_queryset(self):
        comp = self.kwargs['competition']
        return Match.objects.filter(competition=comp)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class FileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    paginator = None


class LinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    paginator = None


class TBMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TBMember.objects.all()
    serializer_class = TBMemberSerializer
    paginator = None


class RefereeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TBMember.objects.filter(referee=True)
    serializer_class = TBMemberSerializer
    paginator = None


class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TBMember.objects.filter(coach=True)
    serializer_class = TBMemberSerializer
    paginator = None
