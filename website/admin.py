from django.contrib import admin
from .models import Post, Team, Match, Competition, Venue, Tag, TBMember

admin.site.site_header = 'Touch Belgium Administration'


# Special one for Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Autosave author (the one who made the request)
    exclude = ('author', 'slug')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        # if getattr(obj, 'slug', None) is None:
        #     obj.slug = slugify(getattr(obj, 'title', None))
        # I am using client side slugs so commenting above
        obj.save()


admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Competition)
admin.site.register(Venue)
admin.site.register(Tag)
admin.site.register(TBMember)
