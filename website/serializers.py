from django.contrib.auth.models import User, Group
from .models import Post, Tag, Venue, Competition, Match, Team
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'url')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture.url)

    class Meta:
        model = Post
        fields = ('id', 'title', 'picture', 'body', 'created_at',
                  'author', 'tags', 'slug')


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url)

    class Meta:
        model = Team
        fields = '__all__'

class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'