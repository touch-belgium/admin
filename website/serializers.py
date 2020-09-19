from django.contrib.auth.models import User, Group
from .models import Tag, Post, Match, Competition, Venue, Club, TBMember, Registration, Event, File, Link, Contact, BannerPicture, Category, Pool, Picture, Gallery, Bonus
from rest_framework import serializers


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(many=False)
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture.url)

    class Meta:
        model = Post
        fields = ('id', 'title', 'picture', 'excerpt', 'body',
                  'created_at', 'author', 'tags')


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ["id"]


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField() # makes the id appear as well
    logo = serializers.SerializerMethodField()
    venue = VenueSerializer()

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url)

    class Meta:
        model = Club
        exclude = ["url"]


class ClubSummarySerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url)

    class Meta:
        model = Club
        fields = ["name", "logo"]


class ClubStatsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    venue = VenueSerializer()

    def get_logo(self, obj):
        return self.context['request'].build_absolute_uri(obj.logo.url)

    class Meta:
        model = Club
        fields = ["name", "logo", "founded", "website", "facebook",
                  "instagram", "venue", "main_belgian_club",
                  "lat", "lng", "n_registered_members", "n_refs",
                  "avg_ref_level", "matches_won", "matches_lost",
                  "matches_tied", "form", "avg_touchdowns_scored",
                  "avg_touchdowns_conceded"]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    home_team = ClubSummarySerializer()
    away_team = ClubSummarySerializer()

    class Meta:
        model = Match
        exclude = ["url", "category"]


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField() # makes the id appear as well

    class Meta:
        model = Competition
        fields = '__all__'
        depth = 1


class PoolSerializer(serializers.ModelSerializer):
    teams = ClubSummarySerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = Pool
        fields = ["name", "teams"]


class BonusSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bonus
        exclude = ["id", "category"]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    matches = MatchSerializer(
        many=True,
        read_only=True
    )
    pools = PoolSerializer(
        many=True,
        read_only=True
    )

    bonuses = BonusSerializer(
        many=True,
        read_only=True
    )

    # BonusSerializer(
    #     many=True,
    #     read_only=True
    # )

    class Meta:
        model = Category
        depth = 5
        fields = ["bonuses", "category", "pools", "matches"]


class CompetitionDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(
        many=True,
        read_only=True
    )

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        full_url = obj.picture
        if obj.picture is not None:
            full_url = self.context['request'].build_absolute_uri(obj.picture.url)
        return full_url

    class Meta:
        model = Competition
        fields = ["name", "competition_type", "social", "start_date",
                  "end_date", "win_value", "tie_value", "defeat_value",
                  "venue", "description", "belgian_championship",
                  "picture", "categories"]
        depth = 2


class TBMemberSerializer(serializers.HyperlinkedModelSerializer):
    picture = serializers.SerializerMethodField()
    club = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    def get_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture.url)

    class Meta:
        model = TBMember
        exclude = ["url"]


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    club = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Club.objects.all(),
        # Following two options allow for independent, no-club
        # registrations on Touch Belgium
        required=False,
        allow_null=True
    )

    class Meta:
        model = Registration
        exclude = ["url"]
        # extra_kwargs = {"season": {"write_only": True},
        #                 "name": {"write_only": True},
        #                 "license_number": {"write_only": True},
        #                 "email": {"write_only": True},
        #                 "dob": {"write_only": True},
        #                 "media_consent": {"write_only": True},
        #                 "guardian_name": {"write_only": True},
        #                 "guardian_email": {"write_only": True},
        #                 "club": {"write_only": True}}


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


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        return self.context['request'].build_absolute_uri(obj.picture.url)

    class Meta:
        model = Picture
        exclude = ["url", "in_gallery"]


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    # FIXME
    pictures = PictureSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Gallery
        fields = '__all__'
        depth = 3
