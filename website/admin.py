from django.contrib import admin
from .models import Post, Tag, Match, Competition, Venue, Team, TBMember, Event, File
import os
import googlemaps

admin.site.site_header = 'Touch Belgium Administration'
gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

# Overloading
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
        # TODO: exception handling
        if hasattr(obj, "address"):
            geocode_result = gmaps.geocode(getattr(obj, "address"), region="BE")
            obj.lat = geocode_result[0]["geometry"]["location"]["lat"]
            obj.lng = geocode_result[0]["geometry"]["location"]["lng"]
            obj.save()


admin.site.register(Match)
admin.site.register(Competition)
admin.site.register(Venue)
admin.site.register(Tag)
admin.site.register(TBMember)
admin.site.register(Event)
admin.site.register(File)
