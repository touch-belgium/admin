import random

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tag, Post, Venue, Club, Match, TBMember, \
    Event, File, Link, Contact, BannerPicture, Competition, \
    Category, Pool, Picture, Gallery
from .serializers import TagSerializer, PostSerializer, \
    ClubSerializer, CompetitionSerializer, MatchSerializer, VenueSerializer,\
    TBMemberSerializer, EventSerializer, FileSerializer, LinkSerializer, \
    ContactSerializer, ClubStatsSerializer, BannerPictureSerializer, \
    CompetitionDetailSerializer, CategorySerializer, PoolSerializer, \
    PictureSerializer, GallerySerializer
# Create your views here.


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    paginator = None


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    paginator = None
    RECENT = 4

    @action(detail=False)
    def recent(self, request, *arg, **kwargs):
        """Limits the response to 4 posts, useful for not having to send the
        whole blog to the landing page. Called like: 'posts/recent' in
        the API
        """
        recent_posts = self.queryset[:self.RECENT]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    paginator = None


class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    paginator = None

    @action(detail=True)
    def stats(self, request, *arg, **kwargs):
        team = Club.objects.get(pk=kwargs["pk"])
        serializer = ClubStatsSerializer(team, many=False, context={"request": request})
        return Response(serializer.data)


class BelgianClubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.filter(main_belgian_club=True)
    serializer_class = ClubSerializer
    paginator = None


class MemberClubViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.filter(member_club=True)
    serializer_class = ClubSerializer
    paginator = None


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    paginator = None

    def retrieve(self, request, pk=None):
        queryset = Competition.objects.all()
        competition = get_object_or_404(queryset, pk=pk)
        serializer = CompetitionDetailSerializer(competition, context={"request": request})
        return Response(serializer.data)


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


class CommitteeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TBMember.objects.filter(committee_member=True)
    serializer_class = TBMemberSerializer
    paginator = None


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    paginator = None


class BannerPictureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BannerPicture.objects.order_by("?")
    serializer_class = BannerPictureSerializer
    paginator = None


class PictureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    paginator = None


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    paginator = None
