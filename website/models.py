from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from filebrowser.fields import FileBrowseField
from tinymce import HTMLField


class Tag(models.Model):
    word = models.CharField(max_length=35)

    def __str__(self):
        return self.word


class Post(models.Model):
    title = models.CharField(max_length=80)
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
    logo = FileBrowseField(max_length=500, default="base/team_placeholder.png",
                           directory="/")
    founded = models.CharField(max_length=4, blank=True, help_text="Year in YYYY format")
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    main_belgian_club = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    competition = models.ForeignKey('Competition', on_delete=models.PROTECT)
    home_team = models.ForeignKey('Team', on_delete=models.PROTECT,
                                  related_name="home_team")
    away_team = models.ForeignKey('Team', on_delete=models.PROTECT,
                                  related_name="away_team")
    when = models.DateTimeField(help_text="Type the time in HH:MM format")
    pitch = models.CharField(max_length=50, blank=True, null=True)
    refs = models.CharField(max_length=100, blank=True, null=True)

    home_touchdowns = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    home_bonus = models.IntegerField(blank=True, default=0)
    away_touchdowns = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    away_bonus = models.IntegerField(blank=True, default=0)
    invitational_match = models.BooleanField()

    def __str__(self):
        return self.competition.name + ", "  + self.home_team.name + \
            ' - ' + self.away_team.name + " | " + \
            self.when.strftime("%d %b %H:%M")

    class Meta:
        verbose_name_plural = "matches"
        ordering = ['-when']


class Competition(models.Model):
    name = models.CharField(max_length=50)
    win_value = models.IntegerField(default=3, validators=[MinValueValidator(0)])
    defeat_value = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    tie_value = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    venue = models.ForeignKey('Venue', on_delete=models.PROTECT,
                              blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TBMember(models.Model):
    name = models.CharField(max_length=100)
    picture = FileBrowseField(max_length=500, default="base/person_placeholder.png",
                              directory="/", blank=True)
    license_number = models.CharField(max_length=30, blank=True)
    team = models.ForeignKey('Team', on_delete=models.PROTECT, blank=True, null=True)

    # Committee
    board_member = models.BooleanField()
    board_position = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Ref
    referee = models.BooleanField(blank=True, null=True)
    referee_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)], blank=True, null=True, default=1)

    referee_board_member = models.BooleanField(blank=True, null=True)
    referee_board_position = models.CharField(max_length=50, blank=True, null=True)

    # Coach
    coach = models.BooleanField(blank=True, null=True)
    coach_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], blank=True, null=True)
    coach_position = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name if not self.referee else self.name + " (ref)"

    class Meta:
        verbose_name = "Touch Belgium member"
        verbose_name_plural = "Touch Belgium members"


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT, blank=True, null=True)


class File(models.Model):
    title = models.CharField(max_length=100)
    file = FileBrowseField(max_length=500, default="base/base_document.pdf", directory="/")
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.title
