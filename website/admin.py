from django.contrib import admin
from .models import Post, Tag, Venue, Team, Match, TBMember, Event, File, Link, Contact, BannerPicture, League, Tournament, Pool, Bonus
from .forms import BonusForm, MatchForm
import os
import googlemaps

admin.site.site_header = 'Touch Belgium Administration'
gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

# Overloading
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("author",)
    exclude = ('author', 'slug')

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
            print("aqui")
            geocode_result = gmaps.geocode(getattr(obj, "venue").address, region="BE")
            print(geocode_result)
            if geocode_result:
                obj.lat = geocode_result[0]["geometry"]["location"]["lat"]
                obj.lng = geocode_result[0]["geometry"]["location"]["lng"]
        obj.save()


@admin.register(TBMember)
class TBMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "referee", "referee_level", "coach")
    list_filter = ("team", "referee", "referee_level", "coach")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "link")
    list_filter = ("tag",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


class MatchAdmin(admin.TabularInline):
    model = Match
    form = MatchForm


class PoolAdmin(admin.StackedInline):
    model = Pool
    extra = 1


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    inlines = [MatchAdmin]
    list_display = ("name", "venue")


class BonusAdmin(admin.TabularInline):
    model = Bonus
    form = BonusForm


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    inlines = [PoolAdmin, MatchAdmin, BonusAdmin]
    list_display = ("name", "venue")


admin.site.register(Venue)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(File)
admin.site.register(BannerPicture)
