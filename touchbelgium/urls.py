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


router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'venues', views.VenueViewSet)
router.register(r'clubs', views.ClubViewSet)
router.register(r'belgian_clubs', views.BelgianClubViewSet, basename="belgian_clubs")
router.register(r'member_clubs', views.MemberClubViewSet, basename="member_clubs")
router.register(r'competitions', views.CompetitionViewSet)
router.register(r'files', views.FileViewSet)
# Members should not be public (or at least hide name, email and dob)
# router.register(r'members', views.TBMemberViewSet, basename="member")
router.register(r'registrations', views.RegistrationViewSet)
router.register(r'referees', views.RefereeViewSet, basename="referee")
router.register(r'coaches', views.CoachViewSet, basename="coach")
router.register(r'committee', views.CommitteeViewSet)
router.register(r'links', views.LinkViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'banner_pictures', views.BannerPictureViewSet)
router.register(r'pictures', views.PictureViewSet)
router.register(r'galleries', views.GalleryViewSet)


urlpatterns = [
    path('filebrowser/', site.urls),
    path('', admin.site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
    path('api/', include(router.urls)),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    re_path(r'^nested_admin/', include('nested_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# That last + static line allows media to be served during development
# see
# https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-files-uploaded-by-a-user-during-development
