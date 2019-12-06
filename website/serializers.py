from django.contrib.auth.models import User, Group
from .models import Post, Tag, Match, Competition, Venue, Team, TBMember, Event, File, Link, Contact, BannerPicture, Category
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
                  'author', 'tags')


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField() # makes the id appear as well
    logo = serializers.SerializerMethodField()
    venue = VenueSerializer()

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url)

    class Meta:
        model = Team
        fields = '__all__'


class TeamSummarySerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url)

    class Meta:
        model = Team
        fields = ["name", "logo"]



class TeamStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name"]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    home_team = TeamSummarySerializer()
    away_team = TeamSummarySerializer()

    class Meta:
        model = Match
        exclude = ["url", "category"]


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField() # makes the id appear as well

    class Meta:
        model = Competition
        fields = '__all__'
        depth = 1


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    matches = MatchSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = Category
        fields = ["category", "matches"]


class CompetitionDetailSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Competition
        fields = ["name", "competition_type", "categories"]
        depth = 2


class TBMemberSerializer(serializers.HyperlinkedModelSerializer):
    picture = serializers.SerializerMethodField()
    team = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    def get_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture.url)

    class Meta:
        model = TBMember
        fields = '__all__'


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class FileSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        return self.context['request'].build_absolute_uri(obj.file.url)

    tag = TagSerializer(read_only=True)

    class Meta:
        model = File
        fields = '__all__'


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    tag = TagSerializer(read_only=True)

    class Meta:
        model = Link
        fields = '__all__'


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class BannerPictureSerializer(serializers.HyperlinkedModelSerializer):
    tag = TagSerializer(read_only=True)
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture.url)

    class Meta:
        model = BannerPicture
        fields = '__all__'
