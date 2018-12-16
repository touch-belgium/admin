from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from filebrowser.fields import FileBrowseField
from tinymce import HTMLField


class Tag(models.Model):
    word = models.CharField(max_length=35)

    def __str__(self):
        return self.word


class Post(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    picture = FileBrowseField(max_length=500, default="base/news_placeholder.png",
                              directory="/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    body = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        out = self.title
        if self.author is not None:
            out += ", by "
            out += self.author.username
        return out

    class Meta:
        get_latest_by = ['-created_at']
        ordering = ['-created_at']


class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = FileBrowseField(max_length=500, default="base/team-placeholder.png",
                           directory="/")
    created = models.CharField(max_length=4, blank=True, help_text="Year in YYYY format")
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    main_belgian_club = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey('Team', on_delete=models.PROTECT,
                                  related_name="home_team")
    away_team = models.ForeignKey('Team', on_delete=models.PROTECT,
                                  related_name="away_team")
    when = models.DateTimeField(help_text="Type the time in HH:MM format")
    pitch = models.CharField(max_length=50, blank=True, null=True)

    home_touchdowns = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    away_touchdowns = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.when.strftime("%d %b %H:%M") + " | " + \
            self.home_team.name + ' - ' + self.away_team.name

    class Meta:
        verbose_name_plural = "matches"


class BoardMember(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name + ' - ' + self.position


class Competition(models.Model):
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField('Team')
    win_value = models.IntegerField(default=3, validators=[MinValueValidator(0)])
    defeat_value = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    tie_value = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    venue = models.ForeignKey('Venue', on_delete=models.PROTECT,
                              blank=True, null=True)

    def __str__(self):
        return self.name
