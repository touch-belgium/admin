"""touchbelgium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings
from filebrowser.sites import site

from rest_framework import routers

from website import views
from website import site_views


api_routes = routers.DefaultRouter()
api_routes.register(r'posts', views.PostViewSet)
api_routes.register(r'tags', views.TagViewSet)
api_routes.register(r'venues', views.VenueViewSet)
api_routes.register(r'clubs', views.ClubViewSet)
api_routes.register(r'belgian_clubs', views.BelgianClubViewSet, basename="belgian_clubs")
api_routes.register(r'member_clubs', views.MemberClubViewSet, basename="member_clubs")
api_routes.register(r'competitions', views.CompetitionViewSet)
api_routes.register(r'files', views.FileViewSet)
# Members should not be public (or at least hide name, email and dob)
# api_routes.register(r'members', views.TBMemberViewSet, basename="member")
api_routes.register(r'registrations', views.RegistrationViewSet)
api_routes.register(r'referees', views.RefereeViewSet, basename="referee")
api_routes.register(r'coaches', views.CoachViewSet, basename="coach")
api_routes.register(r'committee', views.CommitteeViewSet)
api_routes.register(r'links', views.LinkViewSet)
api_routes.register(r'contacts', views.ContactViewSet)
api_routes.register(r'banner_pictures', views.BannerPictureViewSet)
api_routes.register(r'pictures', views.PictureViewSet)
api_routes.register(r'galleries', views.GalleryViewSet)

urlpatterns = [
    path('filebrowser/', site.urls),
    path('', admin.site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
    path('api/', include(api_routes.urls)),
    path('registrations', site_views.registrations_usage),
    path('registrations/approve/', site_views.registrations_approve),
    path('registrations/reject/', site_views.registrations_reject),
    path('registrations/<str:token>/', site_views.registrations),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    re_path(r'^nested_admin/', include('nested_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# That last + static line allows media to be served during development
# see
# https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-files-uploaded-by-a-user-during-development
