from django.contrib import admin
from .models import Tag, Post, Venue, Team, Match, TBMember, Event, File, Link, Contact, BannerPicture, Pool, Bonus, Category, Competition, Picture, Gallery
from .forms import PostForm, BonusForm, MatchForm, PoolForm, TBMemberForm
import os
import googlemaps
import nested_admin

admin.site.site_header = 'Touch Belgium Administration'
gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
        if not hasattr(obj, "author"):
            obj.author = request.user
        # if getattr(obj, 'slug', None) is None:
        #     obj.slug = slugify(getattr(obj, 'title', None))
        # I am using client side slugs so commenting above
        obj.save()


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "main_belgian_club")
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


@admin.register(TBMember)
class TBMemberAdmin(admin.ModelAdmin):
    form = TBMemberForm
    list_display = ("name", "team", "referee", "referee_level", "coach")
    list_filter = ("team", "referee", "referee_level", "coach")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "link")
    list_filter = ("tag",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
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
class CompetitionAdmin(nested_admin.NestedModelAdmin):
    inlines = [CategoryAdmin]
    list_display = ("name", "venue")
    list_filter = ("belgian_championship",)


class PictureAdmin(nested_admin.NestedStackedInline):
    model = Picture


@admin.register(Gallery)
class GalleryAdmin(nested_admin.NestedModelAdmin):
    inlines = [PictureAdmin]


admin.site.register(Venue)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(File)
admin.site.register(BannerPicture)
