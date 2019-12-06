from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
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
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
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
    venue = models.ForeignKey("Venue", on_delete=models.PROTECT, blank=True, null=True)
    main_belgian_club = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="matches")
    home_team = models.ForeignKey("Team", on_delete=models.PROTECT,
                                  related_name="home_team")
    away_team = models.ForeignKey("Team", on_delete=models.PROTECT,
                                  related_name="away_team")
    when = models.DateTimeField(help_text="Type the time in HH:MM format")
    pitch = models.CharField(max_length=50, blank=True, null=True)
    refs = models.CharField(max_length=100, blank=True, null=True)

    home_touchdowns = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    away_touchdowns = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    POOL_STAGE = "PS"
    RANK_STAGE = "RS"
    PLAYOFF = "PO"
    QUARTER_FINAL = "QF"
    SEMI_FINAL = "SF"
    FINAL = "FF"
    MATCH_CHOICES = [
        (POOL_STAGE, "Pool match"),
        (RANK_STAGE, "Ranking match"),
        (PLAYOFF, "Playoff"),
        (QUARTER_FINAL, "Quarter final"),
        (SEMI_FINAL, "Semi final"),
        (FINAL, "Final")
    ]
    match_type = models.CharField(max_length=2, choices=MATCH_CHOICES, blank=True, help_text="Leave blank for league style competitions")
    invitational_match = models.BooleanField(default=False, verbose_name="invitational match ?")

    @property
    def match(self):
        return self.home_team.name + ' vs ' + self.away_team.name


    def __str__(self):
        return self.home_team.name + \
            ' - ' + self.away_team.name + " | " + \
            self.match_type

    class Meta:
        verbose_name_plural = "matches"
        ordering = ['-when']


class Competition(models.Model):
    name = models.CharField(max_length=50)
    POOL_AND_RANK = "PR"
    POOL_AND_PLAYOFF = "PP"
    LEAGUE = "LL"
    COMPETITION_CHOICES = [
        (POOL_AND_RANK, "Two stages: pools and rank"),
        (POOL_AND_PLAYOFF, "Two stages: pools and playoff matches"),
        (LEAGUE, "League: point based system")
    ]
    competition_type = models.CharField(max_length=2, choices=COMPETITION_CHOICES)
    win_value = models.IntegerField(default=4, validators=[MinValueValidator(0)])
    tie_value = models.IntegerField(default=2, validators=[MinValueValidator(0)])
    defeat_value = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    venue = models.ForeignKey('Venue', on_delete=models.PROTECT,
                              blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    belgian_championship = models.BooleanField(default=False, verbose_name="belgian national championship ?")

    @property
    def n_participating_teams(self):
        matches = Match.objects.filter(competition=self)
        different_teams = set()
        for match in matches:
            different_teams.add(match.home_team)
            different_teams.add(match.away_team)
        return len(different_teams)

    @property
    def participating_teams(self):
        matches = Match.objects.filter(competition=self)
        different_teams = set()
        for match in matches:
            different_teams.add(match.home_team)
            different_teams.add(match.away_team)
        return different_teams


    def __str__(self):
        return self.name


class Bonus(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    points = models.IntegerField(help_text="Bonus points can be negative")

    class Meta:
        verbose_name_plural = "Bonuses"


class Category(models.Model):
    MEN_OPEN = "MO"
    WOMEN_OPEN = "WO"
    MIXED_OPEN = "XO"
    MEN_27 = "M27"
    WOMEN_27 = "W27"
    MIXED_27 = "X27"
    MEN_30 = "M30"
    WOMEN_30 = "W30"
    MIXED_30 = "X30"
    MEN_40 = "M30"
    WOMEN_40 = "W30"
    MIXED_40 = "X40"
    JUNIOR = "JO"

    CATEGORY_CHOICES = [
        (MEN_OPEN, "MO"),
        (WOMEN_OPEN, "WO"),
        (MIXED_OPEN, "XO"),
        (MEN_27, "M27"),
        (WOMEN_27, "W27"),
        (MIXED_27, "X27"),
        (MEN_30, "M30"),
        (WOMEN_30, "W30"),
        (MIXED_30, "X30"),
        (MEN_40, "M40"),
        (WOMEN_40, "W40"),
        (MIXED_40, "X40"),
        (JUNIOR, "JO")
    ]
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, help_text="Men open, women open, mixed open...")
    competition = models.ForeignKey("Competition", on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class Pool(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="pools")
    name = models.CharField(max_length=50, help_text="Do not create any pools for a league type competition")
    teams = models.ManyToManyField("Team")

    def __str__(self):
        return self.name


class TBMember(models.Model):
    name = models.CharField(max_length=100)
    picture = FileBrowseField(max_length=500, default="base/person_placeholder.png",
                              directory="/", blank=True)
    license_number = models.CharField(max_length=30, blank=True)
    team = models.ForeignKey('Team', on_delete=models.PROTECT, blank=True, null=True)

    # Committee
    committee_member = models.BooleanField()
    committee_position = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    committee_text = models.TextField(blank=True, null=True)

    # Ref
    referee = models.BooleanField(blank=True, null=True)
    referee_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)], blank=True, null=True, default=1)

    referee_board_member = models.BooleanField(blank=True, null=True)
    referee_board_position = models.CharField(max_length=50, blank=True, null=True)
    referee_text = models.TextField(blank=True, null=True)

    # Coach
    coach = models.BooleanField(blank=True, null=True)
    coach_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], blank=True, null=True)
    coach_position = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.name

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
        return self.tag.word.upper() + " - " + self.title


class Link(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "{} - ({})".format(self.title, self.tag.word)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class BannerPicture(models.Model):
    picture = FileBrowseField(max_length=500)
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "{} banner picture - #{}".format(self.tag.word.upper(), self.id)
