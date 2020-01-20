from django import forms
from dal import autocomplete

from .models import Post, Bonus, Match, Pool, TBMember

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('__all__')
        widgets = {
            "home_team": autocomplete.ModelSelect2(),
            "away_team": autocomplete.ModelSelect2()
        }

class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = ('__all__')
        widgets = {
            "team": autocomplete.ModelSelect2()
        }


class PoolForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = ('__all__')
        widgets = {
            "teams": autocomplete.ModelSelect2Multiple()
        }


class TBMemberForm(forms.ModelForm):
    class Meta:
        model = TBMember
        fields = ('__all__')
        widgets = {
            "team": autocomplete.ModelSelect2()
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'slug')
        widgets = {
            "tags": autocomplete.ModelSelect2Multiple()
        }
