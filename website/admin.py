from django.contrib import admin
from django.utils import timezone
from reversion.admin import VersionAdmin

from .models import Tag, Post, Venue, Club, BelgianClub, Match, TBMember, Registration, Event, File, Link, Contact, BannerPicture, Pool, Bonus, Category, Competition, Picture, Gallery
from .forms import PostForm, BonusForm, MatchForm, PoolForm, TBMemberForm, RegistrationForm
import os
import googlemaps
import nested_admin

admin.site.site_title = "Touch Belgium site admin"
admin.site.site_header = "Touch Belgium Administration"
admin.site.site_url = "https://touch-belgium.be"

gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

@admin.register(Post)
class PostAdmin(VersionAdmin):
    form = PostForm
    list_display = ("title", "author", "created_at")
    list_filter = ("author",)

    # Method override
    def save_model(self, request, obj, form, change):
        """request - The HTTP request
        obj - The model instance
        form - a ModelForm instance
        change - boolean set to True if updating instead of creating the object
        This override will auto-save the author (the one who made the
        request)
        """
        if getattr(obj, "author", None) is None:
            obj.author = request.user
        if getattr(obj, "pk", None) is None:
            # When first creating the post
            obj.created_at = timezone.now()
        obj.updated_at = timezone.now()
        obj.save()


@admin.register(Club)
class ClubAdmin(VersionAdmin):
    list_display = ("name", "venue")
    # Lat and long will be given by the Geocoding API, no need to show
    # them on the admin interface
    exclude = ('lat', 'lng')

    def save_model(self, request, obj, form, change):
        """request - The HTTP request
        obj - The model instance
        form - a ModelForm instance
        change - boolean set to True if updating instead of creating the object

        This override fetches the address coordinates from Google's
        Geocoding API and saves them.

        """
        if getattr(obj, "venue", None) is not None:
            geocode_result = gmaps.geocode(getattr(obj, "venue").address, region="BE")
            if geocode_result:
                obj.lat = geocode_result[0]["geometry"]["location"]["lat"]
                obj.lng = geocode_result[0]["geometry"]["location"]["lng"]
        obj.save()


@admin.register(BelgianClub)
class BelgianClubAdmin(ClubAdmin):
    pass


@admin.register(TBMember)
class TBMemberAdmin(VersionAdmin):
    form = TBMemberForm
    list_display = ("name", "club", "referee", "referee_level", "coach")
    list_filter = ("club", "referee", "referee_level", "coach")


@admin.register(Registration)
class RegistrationAdmin(VersionAdmin):
    form = RegistrationForm
    list_display = ("name", "email", "season", "club", "dob")
    list_filter = ("name", "email", "season", "club")


@admin.register(Link)
class LinkAdmin(VersionAdmin):
    list_display = ("title", "tag", "link")
    list_filter = ("tag",)


@admin.register(Contact)
class ContactAdmin(VersionAdmin):
    list_display = ("name", "email")


class MatchAdmin(nested_admin.NestedStackedInline):
    model = Match
    form = MatchForm
    extra = 2


class PoolAdmin(nested_admin.NestedStackedInline):
    model = Pool
    form = PoolForm
    extra = 1


class BonusAdmin(nested_admin.NestedStackedInline):
    model = Bonus
    form = BonusForm
    extra = 1


class CategoryAdmin(nested_admin.NestedStackedInline):
    model = Category
    inlines = [PoolAdmin, MatchAdmin, BonusAdmin]
    extra = 1


@admin.register(Competition)
class CompetitionAdmin(VersionAdmin, nested_admin.NestedModelAdmin):
    inlines = [CategoryAdmin]
    list_display = ("name", "venue")
    list_filter = ("belgian_championship",)


class PictureAdmin(nested_admin.NestedStackedInline):
    model = Picture


@admin.register(Gallery)
class GalleryAdmin(VersionAdmin, nested_admin.NestedModelAdmin):
    inlines = [PictureAdmin]


admin.site.register(Venue)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(File)
admin.site.register(BannerPicture)
